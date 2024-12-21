from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin, Environment, User
from web_backend.schemas import (
    EnvironmentPublic,
    ExistingUser,
    Message,
    UserPatch,
    UserPublic,
    UserSchema,
    UserUpdated,
)
from web_backend.security import get_current_admin
from web_backend.utils.user import (
    upload_photo,
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
    user_form: Annotated[UserSchema, Depends(UserSchema)],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
    file: Annotated[UploadFile | str, File()] = None,
    environment_ids: Annotated[list[int] | None, Form()] = None,
):
    if not verify_repeated_fields(user_form, session):
        user_db = User(
            registered_by_admin_id=current_admin.id,
            name=user_form.name,
            email=user_form.email,
            date_of_birth=user_form.date_of_birth,
            cpf=user_form.cpf,
            phone_number=user_form.phone_number,
        )

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

    photo = ''
    if not isinstance(file, str):
        photo = file.filename

    existing_ids, invalid_environment_ids = verify_environment_ids(
        environment_ids, session, user_db
    )

    user_public = UserPublic.model_validate(user_db)

    return {
        'message': 'User created sucessfully',
        'user_created': user_public,
        'photo': photo,
        'environment_ids': existing_ids,
        'invalid_environment_ids': invalid_environment_ids,
    }


@router.delete(
    path='/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
)
def delete_user(
    user_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
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
)
def get_users(
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Page[UserPublic]:
    query = select(User).order_by(User.registered_at)
    return paginate(session, query)


@router.patch(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserUpdated,
    responses={
        HTTPStatus.NOT_FOUND: {'model': Message},
        HTTPStatus.CONFLICT: {'model': ExistingUser},
    },
)
def patch_user(
    user_id: int,
    user_schema: UserPatch,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
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

        user_public = UserPublic(
            name=user_db.name,
            email=user_db.email,
            date_of_birth=user_db.date_of_birth,
            cpf=user_db.cpf,
            phone_number=user_db.phone_number,
            id=user_db.id,
        )

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
)
def get_user_enviroments(
    user_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
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


@router.post(path='/upload-image/{user_id}')
def perfil_photo_upload(
    user_id: int,
    file: Annotated[UploadFile, File()],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
):
    if not upload_photo(file, user_id):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"File for user '{user_id}' already exists!",
        )

    return {
        'message': 'Image uploaded successfully!',
        'filename': file.filename,
    }
