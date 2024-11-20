from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.database import get_session
# from web_backend.models import User
from web_backend.schemas import (
    Message
)
from web_backend.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/workers', tags=['workers'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Message,
)
def create_user(
    user: Message, session: Annotated[Session, Depends(get_session)]
) -> Message:
    # db_user = session.scalar(
    #     select(User).where(
    #         (User.username == user.username) | (User.email == user.email)
    #     )
    # )
    # if db_user:
    #     if db_user.username == user.username and db_user.email == user.email:
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST,
    #             detail='Username and email already exists',
    #         )
    #     elif db_user.username == user.username:
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST,
    #             detail='Username already exists',
    #         )
    #     elif db_user.email == user.email:
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST,
    #             detail='Email already exists',
    #         )

    # db_user = User(
    #     username=user.username,
    #     password=get_password_hash(user.password),
    #     email=user.email,
    # )
    ...

    # session.add(db_user)
    # session.commit()
    # session.refresh(db_user)

    return {'message': 'qualquer coisa'}


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Message, Depends(get_current_user)],
) -> Message:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted successfully'}


@router.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_users(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
) -> Message:
    # users = session.scalars(select(User).offset(skip).limit(limit)).all()
    # return {'users': users}
    return {'message': 'Nada ainda'}


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def update_user(
    user_id: int,
    upd_user: Message,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Message, Depends(get_current_user)],
) -> Message:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    current_user.username = upd_user.username
    current_user.email = upd_user.email
    current_user.password = get_password_hash(upd_user.password)
    current_user.status = upd_user.status

    session.commit()
    session.refresh(current_user)

    return current_user
