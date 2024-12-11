from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin, Enviroment
from web_backend.schemas import (
    EnviromentPublic,
    Enviroments,
    EnviromentSchema,
    EnviromentUpdated,
    Message,
)
from web_backend.security import get_current_admin

router = APIRouter(prefix='/enviroments', tags=['enviroments'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=EnviromentPublic,
    responses={
        HTTPStatus.CONFLICT: {'model': Message},
        HTTPStatus.UNAUTHORIZED: {'model': Message},
    },
)
def create_enviroment(
    enviroment: EnviromentSchema,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> EnviromentPublic:
    enviroment_db = session.scalar(
        select(Enviroment).where(Enviroment.name == enviroment.name)
    )

    if enviroment_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Enviroment name already in use',
        )

    enviroment_db = Enviroment(
        name=enviroment.name, creator_admin_id=current_admin.id
    )

    session.add(enviroment_db)
    session.commit()
    session.refresh(enviroment_db)

    return enviroment_db


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Enviroments,
)
def get_enviroments(
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Enviroments:
    enviroments = session.scalars(select(Enviroment)).all()
    return {'enviroments': enviroments}


@router.delete(
    path='/{enviroment_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
)
def delete_enviroment(
    enviroment_id: int,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> Message:
    enviroment_db = session.scalar(
        select(Enviroment).where(Enviroment.id == enviroment_id)
    )

    if enviroment_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Enviroment not found'
        )

    session.delete(enviroment_db)
    session.commit()

    return {'message': 'Enviroment deleted successfully!'}


@router.put(
    '/{enviroment_id}',
    status_code=HTTPStatus.OK,
    response_model=EnviromentUpdated,
)
def update_enviroment(
    enviroment_id: int,
    new_enviroment: EnviromentSchema,
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
) -> EnviromentUpdated:
    enviroment_db = session.scalar(
        select(Enviroment).where(Enviroment.id == enviroment_id)
    )

    if enviroment_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Enviroment not found'
        )

    enviroment_db.name = new_enviroment.name
    enviroment_db.updated_at = func.now()
    session.commit()

    return {
        'message': 'Enviroment updated successfully!',
        'enviroment_updated': enviroment_db
    }
