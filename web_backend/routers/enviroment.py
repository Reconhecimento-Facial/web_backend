from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin, Environment
from web_backend.schemas import (
    EnvironmentPublic,
    Environments,
    EnvironmentSchema,
    EnvironmentUpdated,
    Message,
)
from web_backend.security import get_current_admin

router = APIRouter(prefix='/Environments', tags=['Environments'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=EnvironmentPublic,
    responses={
        HTTPStatus.CONFLICT: {'model': Message},
        HTTPStatus.UNAUTHORIZED: {'model': Message},
    },
)
def create_Environment(
    environment: EnvironmentSchema,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> EnvironmentPublic:
    environment_db = session.scalar(
        select(Environment).where(Environment.name == environment.name)
    )

    if environment_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Environment name already in use',
        )

    environment_db = Environment(
        name=environment.name, creator_admin_id=current_admin.id
    )

    session.add(environment_db)
    session.commit()
    session.refresh(environment_db)

    return environment_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Environments,
)
def get_environments(
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Environments:
    environments = session.scalars(select(Environment)).all()
    return {'environments': environments}


@router.delete(
    path='/{Environment_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
)
def delete_Environment(
    environment_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Message:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    session.delete(environment_db)
    session.commit()

    return {'message': 'Environment deleted successfully!'}


@router.put(
    '/{Environment_id}',
    status_code=HTTPStatus.OK,
    response_model=EnvironmentUpdated,
)
def update_Environment(
    Environment_id: int,
    new_environment: EnvironmentSchema,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> EnvironmentUpdated:
    environment_db = session.scalar(
        select(Environment).where(Environment.id == Environment_id)
    )

    if Environment_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    environment_db.name = new_environment.name
    environment_db.updated_at = func.now()
    session.commit()

    return {
        'message': 'Environment updated successfully!',
        'Environment_updated': environment_db,
    }
