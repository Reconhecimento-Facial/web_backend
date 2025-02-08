from datetime import date
from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from unidecode import unidecode

from web_backend.database import get_session
from web_backend.models import Admin, Environment, User
from web_backend.schemas import (
    EnvironmentPublic,
    Message,
    PhotoUploaded,
    UserFilter,
    UserPublic,
    UserPublicWithUrl,
    UserSchema,
    UserSchemaPut,
)
from web_backend.security import get_current_admin
from web_backend.utils.file_path import file_path
from web_backend.utils.upload_photo import upload_photo
from web_backend.utils.user import (
    verify_environment_ids,
    verify_environment_ids_put,
    verify_repeated_fields,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=dict,
    responses={HTTPStatus.CONFLICT: {'model': Message}},
    openapi_extra={
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'encoding': {
                        'environment_ids': {
                            'style': 'form',
                            'explode': True,
                        },
                    },
                },
            },
        },
    },
)
def create_user(
    session: Annotated[Session, Depends(get_session)],
    user_form: Annotated[UserSchema, Depends()],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    photo: Annotated[UploadFile | str, File()] = None,
    environment_ids: Annotated[list[int] | None, Form()] = None,
):
    verify_repeated_fields(user_form, session)

    user_db = User(
        **user_form.model_dump(),
        name_unaccent=unidecode(user_form.name),
        registered_by_admin_id=current_admin.id,
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    photo_ans = ''

    if not isinstance(photo, str):
        photo_ans = photo.filename
        upload_photo(photo, user_db.id, 'users_photos')

    existing_ids, invalid_environment_ids = verify_environment_ids(
        environment_ids, session, user_db
    )

    user_public = UserPublic.model_validate(user_db)

    return {
        'message': 'User created successfully',
        'user_created': user_public,
        'photo': photo_ans,
        'environment_ids': existing_ids,
        'invalid_environment_ids': invalid_environment_ids,
    }


@router.delete(
    path='/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
    dependencies=[Depends(get_current_admin)],
)
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Message:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted successfully!'}


@router.get(
    path='/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicWithUrl,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
    dependencies=[Depends(get_current_admin)],
)
def get_user_by_id(
    user_id: int,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> UserPublicWithUrl:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    file = file_path(user_db.id, 'users_photos')
    user_db.photo_url = ''
    if file:
        user_db.photo_url = str(request.base_url) + file

    return user_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Page[UserPublic],
    dependencies=[Depends(get_current_admin)],
)
def get_users(
    session: Annotated[Session, Depends(get_session)],
    filters: Annotated[UserFilter, Depends()],
) -> Page[UserPublic]:
    query = select(User)
    if filters.name:
        query = query.where(
            User.name_unaccent.ilike(f'%{unidecode(filters.name)}%')
        )

    if filters.status:
        query = query.where(User.status == filters.status)

    column = User.name
    if filters.sort_by:
        column = getattr(User, filters.sort_by.value)

    query = query.order_by(
        desc(column)
        if filters.sort_order == UserFilter.AscendingOrDescending.descending
        else asc(column)
    )

    return paginate(session, query)


@router.get(
    path='/environments/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Page[EnvironmentPublic],
    dependencies=[Depends(get_current_admin)],
)
def get_user_environments(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> Page[EnvironmentPublic]:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    query = (
        select(Environment).join(User.environments).where(User.id == user_id)
    )

    return paginate(session, query)


@router.post(
    path='/upload-image/{user_id}',
    status_code=HTTPStatus.CREATED,
    response_model=PhotoUploaded,
    dependencies=[Depends(get_current_admin)],
)
def perfil_photo_upload(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    photo: Annotated[UploadFile, File()],
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    upload_photo(photo, user_db.id, 'users_photos')

    return {
        'message': 'Image uploaded successfully!',
        'filename': photo.filename,
    }


@router.put(
    path='/{user_id}',
    status_code=HTTPStatus.CREATED,
    response_model=dict,
    responses={HTTPStatus.CONFLICT: {'model': Message}},
    openapi_extra={
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'encoding': {
                        'environment_ids': {
                            'style': 'form',
                            'explode': True,
                        },
                    },
                },
            },
        },
    },
    dependencies=[Depends(get_current_admin)],
)
def update_user(  # noqa PLR0913
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    request: Request,
    user_form: Annotated[UserSchemaPut, Depends()],
    photo: Annotated[UploadFile | str, File()] = None,
    environment_ids: Annotated[list[int] | None, Form()] = None,
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    verify_repeated_fields(user_form, session)

    for field, value in user_form.model_dump(exclude_unset=True).items():
        if not (
            value == 'default@default.com'
            or value == date(1, 1, 1)
            or not value
        ):
            setattr(user_db, field, value)

    session.commit()
    session.refresh(user_db)

    if not isinstance(photo, str):
        upload_photo(photo, user_db.id, 'users_photos')

    photo_url = file_path(user_db.id, 'users_photos')
    if photo_url:
        photo_url = str(request.base_url) + photo_url

    existing_ids, invalid_environment_ids = verify_environment_ids_put(
        environment_ids, session, user_db
    )

    user_public = UserPublic.model_validate(user_db)

    return {
        'message': 'User updated successfully',
        'user_created': user_public,
        'photo_url': photo_url,
        'environment_ids': existing_ids,
        'invalid_environment_ids': invalid_environment_ids,
    }
