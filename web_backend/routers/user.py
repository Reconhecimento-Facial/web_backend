from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, asc, desc, or_, select
from sqlalchemy.orm import Session
from unidecode import unidecode

from web_backend.database import get_session
from web_backend.models import Admin, Environment, User
from web_backend.schemas import (
    EnvironmentPublic,
    ExistingUser,
    Message,
    PhotoUploaded,
    UserFilter,
    UserPatch,
    UserPublic,
    UserSchema,
    UserUpdated,
)
from web_backend.security import get_current_admin
from web_backend.utils.upload_photo import upload_photo
from web_backend.utils.user import (
    verify_environment_ids,
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
        'message': 'User created sucessfully',
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

    return {'message': 'User deleted sucessfully!'}


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

    if filters.sort_by:
        column = getattr(User, filters.sort_by.value.lower())
        query = query.order_by(
            desc(column)
            if filters.sort_order
            == UserFilter.AscendingOrDescending.descending
            else asc(column)
        )

    return paginate(session, query)


@router.patch(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserUpdated,
    responses={
        HTTPStatus.NOT_FOUND: {'model': Message},
        HTTPStatus.CONFLICT: {'model': ExistingUser},
    },
    dependencies=[Depends(get_current_admin)],
)
def patch_user(
    user_id: int,
    user_schema: UserPatch,
    session: Annotated[Session, Depends(get_session)],
) -> UserUpdated:
    user_db = session.scalar(
        select(User).where(
            and_(
                or_(
                    User.email == user_schema.email,
                    User.cpf == user_schema.cpf,
                    User.phone_number == user_schema.phone_number,
                ),
                User.id != user_id,
            )
        )
    )

    if user_db:
        message = ' already in use!'
        if user_db.email == user_schema.email:
            message = 'Email' + message
        elif user_db.cpf == user_schema.cpf:
            message = 'CPF' + message
        elif user_db.phone_number == user_schema.phone_number:
            message = 'Phone Number' + message

        user_public = UserPublic.model_validate(user_db)
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail={'message': message, 'existing_user': user_public},
        )

    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found!'
        )

    for key, value in user_schema.model_dump(exclude_unset=True).items():
        setattr(user_db, key, value)

    session.commit()
    session.refresh(user_db)
    return {'message': 'User updated sucessfully', 'user_updated': user_db}


@router.get(
    path='/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Page[EnvironmentPublic],
    dependencies=[Depends(get_current_admin)],
)
def get_user_enviroments(
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
