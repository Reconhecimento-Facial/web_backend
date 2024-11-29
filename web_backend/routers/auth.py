from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.database import get_session
from web_backend.models import Admin
from web_backend.schemas import (
    Token,
)
from web_backend.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=Token,
)
def login_for_admin_token(
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    ...
    admin = session.scalar(
        select(Admin).where(Admin.email == form_data.username)
    )

    if not admin:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': admin.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
