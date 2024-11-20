from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from web_backend.database import get_session
from web_backend.models import Admin
from web_backend.schemas import AdminSchema, Message

router = APIRouter(prefix='/admins', tags=['admins'])


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=Message
)
def create_admin(
    admin: AdminSchema, 
    session: Annotated[Session, Depends(get_session)]
) -> Message:
    
    admin_db = Admin(
        username=admin.username,
        password=admin.password,
        super_admin=admin.super_admin
    )

    session.add(admin_db)
    session.commit()
    
    return {'message': 'Admin created succesfully!'}


