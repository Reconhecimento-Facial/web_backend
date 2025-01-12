from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin, Device, Environment
from web_backend.schemas import DeviceSchema, Message
from web_backend.security import get_current_admin

router = APIRouter(prefix='/devices', tags=['devices'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    responses={HTTPStatus.NOT_FOUND: {'model': Message}},
    response_model=DeviceSchema,
)
def create_device(
    current_admin: Annotated[Admin, Depends(get_current_admin)],
    session: Annotated[Session, Depends(get_session)],
    environment_id: int,
    serial_number: str,
) -> DeviceSchema:
    environment = session.scalar(
        select(Environment).where(Environment.id == environment_id)
    )

    if environment is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
        )

    device = Device(
        serial_number=serial_number,
        environment_id=environment_id,
        environment=environment,
        creator_admin_id=current_admin.id,
    )

    session.add(device)
    session.commit()
    session.refresh(device)

    return device
