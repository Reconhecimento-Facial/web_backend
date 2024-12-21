import shutil
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.models import Environment, User
from web_backend.schemas import UserSchema


def upload_photo(file: UploadFile, user_id: int) -> bool:
    upload_dir = Path.cwd() / 'uploads' / 'users_photos'
    upload_dir.mkdir(parents=True, exist_ok=True)

    extensao = Path(file.filename).suffix
    nome_arquivo = f'{user_id}{extensao}'
    file_path = upload_dir / nome_arquivo

    if file_path.exists():
        return False

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return True


def verify_repeated_fields(user_form: UserSchema, session: Session) -> bool:
    user_db = session.scalar(
        select(User).where(
            (User.email == user_form.email)
            | (User.cpf == user_form.cpf)
            | (User.phone_number == user_form.phone_number)
        )
    )

    if user_db:
        http_exception = HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=' already in use!'
        )
        if user_db.email == user_form.email:
            http_exception.detail = 'Email' + http_exception.detail
            raise http_exception
        elif user_db.cpf == user_form.cpf:
            http_exception.detail = 'CPF' + http_exception.detail
            raise http_exception
        elif user_db.phone_number == user_form.phone_number:
            http_exception.detail = 'Phone Number' + http_exception.detail
            raise http_exception

    return False


def verify_environment_ids(
    environment_ids: list[int] | None, session: Session, user_db: User
) -> tuple[list[int], list[int]]:
    if environment_ids is None:
        return [], []

    existing_environments = session.scalars(
        select(Environment).where(Environment.id.in_(environment_ids))
    ).all()

    existing_ids = [env.id for env in existing_environments]
    invalid_ids = [
        env_id for env_id in environment_ids if env_id not in existing_ids
    ]

    for environment in existing_environments:
        user_db.environments.append(environment)

    session.commit()

    return existing_ids, invalid_ids
