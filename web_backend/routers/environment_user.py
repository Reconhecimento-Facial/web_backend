from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin, Environment, User
from web_backend.schemas import (
    EnvironmentAdded,
    Message,
)
from web_backend.security import get_current_admin

router = APIRouter(prefix='/users_environments', tags=['users_evironments'])


@router.post(
    '/{user_id}/{environment_id}',
    response_model=EnvironmentAdded,
)
def add_environment_permission(
    user_id: int,
    environment_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> EnvironmentAdded:
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    env_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if env_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found!'
        )

    if env_db in user_db.environments:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User already has this environment!',
        )

    user_db.environments.append(env_db)
    session.commit()
    session.refresh(user_db)

    return EnvironmentAdded(
        message='Environment added successfully',
        environment_added={'id': env_db.id, 'name': env_db.name},
    )


@router.delete(
    path='{user_id}/{environment_id}',
    response_model=Message,
)
def remove_environment_permission(
    user_id: int,
    environment_id: int,
    session: Annotated[Session, Depends(get_session)]
) -> Message:
    
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    env_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if env_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found!'
        )

    if env_db not in user_db.environments:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User does not have this environment!',
        )
    
    user_db.environments.remove(env_db)
    session.commit()
    session.refresh(user_db)

    return {'message': 'Environment removed from user successfully!'}