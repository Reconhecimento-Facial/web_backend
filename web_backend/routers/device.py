from http import HTTPStatus
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
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
    serial_number: str,
    environment_id: int | None = None,
) -> DeviceSchema:
    
    environment = None
    if environment_id:
        environment = session.scalar(
            select(Environment).where(Environment.id == environment_id)
        )

        if environment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Environment not found'
            )

    device = session.scalar(
        select(Device).where(Device.serial_number == serial_number)
    )

    if device:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='A device with this serial number already exists.',
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


@router.get(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Page[DeviceSchema],
    dependencies=[Depends(get_current_admin)],
)
def get_devices(
    session: Annotated[Session, Depends(get_session)],
    serial_number: Optional[str] = Query(
        None, description='Filter by serial number'
    ),
) -> Page[DeviceSchema]:
    query = select(Device)

    if serial_number:
        query = query.where(Device.serial_number.like(f'%{serial_number}%'))

    return paginate(session, query)


@router.delete(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=Message,
    dependencies=[Depends(get_current_admin)],
)
def delete_device(
    session: Annotated[Session, Depends(get_session)],
    id: UUID,
) -> Message:
    device = session.scalar(select(Device).where(Device.id == id))

    if device is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='device not found'
        )

    session.delete(device)
    session.commit()

    return {'message': 'Device deleted successfully'}


@router.put(
    path='/',
    status_code=HTTPStatus.OK,
    response_model=DeviceSchema,
    dependencies=[Depends(get_current_admin)],
)
def update_device(
    id: UUID,
    session: Annotated[Session, Depends(get_session)],
    serial_number: Optional[str] = None,
    environment_id: Optional[int] = None,
) -> DeviceSchema:
    device = session.scalar(select(Device).where(Device.id == id))

    if device is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='device not found'
        )

    if serial_number:
        device.serial_number = serial_number

    if environment_id:
        environment = session.scalar(
            select(Environment).where(Environment.id == environment_id)
        )

        if environment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Environment not found',
            )

        device.environment = environment
        device.environment_id = environment.id

    session.commit()
    session.refresh(device)

    return device


@router.get(
    path='/{device_id}',
    status_code=HTTPStatus.OK,
    response_model=DeviceSchema,
    dependencies=[Depends(get_current_admin)],
)
def get_device_by_id(
    device_id: UUID, session: Annotated[Session, Depends(get_session)]
) -> Device:
    device_db = session.scalar(select(Device).where(Device.id == device_id))

    if device_db is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='device not found'
        )

    return device_db
