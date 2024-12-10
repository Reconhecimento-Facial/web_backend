from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin
from web_backend.schemas import (
    AdminProfile,
    AdminPublic,
    Admins,
    AdminSchema,
    HTTPExceptionResponse,
    Message,
)
from web_backend.security import get_current_admin, get_password_hash

router = APIRouter(prefix='/admins', tags=['admins'])


@router.post(
    path='/', status_code=HTTPStatus.CREATED, response_model=AdminPublic
)
def create_admin(
    admin: AdminSchema,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
) -> Message:
    if not current_admin.super_admin:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough perission'
        )

    admin_db = session.scalar(
        select(Admin).where((Admin.email == admin.email))
    )

    if admin_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already in use'
        )

    admin_db = Admin(
        email=admin.email,
        password=get_password_hash(admin.password),
        super_admin=admin.super_admin,
    )

    session.add(admin_db)
    session.commit()
    session.refresh(admin_db)

    return admin_db


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Admins,
    responses={HTTPStatus.FORBIDDEN: {'model': HTTPExceptionResponse}},
)
def get_admins(
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
) -> Admins:
    if not current_admin.super_admin:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
    admins = session.scalars(select(Admin)).all()
    return {'admins': admins}


@router.delete(
    '/{admin_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={HTTPStatus.FORBIDDEN: {'model': HTTPExceptionResponse}},
)
def delete_admin(
    admin_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Admin, Depends(get_current_admin)],
) -> Message:
    if not current_admin.super_admin:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    admin_db = session.scalar(select(Admin).where(Admin.id == admin_id))

    if not admin_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Admin not found'
        )

    session.delete(admin_db)
    session.commit()

    return {'message': 'Admin deleted successfully'}


@router.get(
    '/profile',
    status_code=HTTPStatus.OK,
    response_model=AdminProfile,
)
def get_admin_profile(current_admin: Admin = Depends(get_current_admin)):
    return current_admin
