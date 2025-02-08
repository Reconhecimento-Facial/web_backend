from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from web_backend.models import Environment, User
from web_backend.schemas import UserSchema


def verify_repeated_fields(user_form: UserSchema, session: Session) -> None:
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


def verify_environment_ids(
    environment_ids: list[int] | None, session: Session, user_db: User
) -> tuple[list[int], list[int]]:
    """
    Verify valid environments and already add them to user.

    Args:
        environment_ids (list[int] | None): List of environment IDs to verify.
        session (Session): SQLAlchemy session object.
        user_db (User): User database object to which environments will be
        added.

    Returns:
        tuple[list[int], list[int]]: A tuple containing two lists:
            - The first list contains the IDs of the valid environments.
            - The second list contains the IDs of the invalid environments.
    """
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


def verify_environment_ids_put(
    environment_ids: list[int] | None, session: Session, user_db: User
) -> tuple[list[int], list[int]]:
    """
    Verify valid environments and already add them to user.

    Args:
        environment_ids (list[int] | None): List of environment IDs to verify.
        session (Session): SQLAlchemy session object.
        user_db (User): User database object to which environments will be
        added.

    Returns:
        tuple[list[int], list[int]]: A tuple containing two lists:
            - The first list contains the IDs of the valid environments.
            - The second list contains the IDs of the invalid environments.
    """
    if environment_ids is None:
        return [], []

    existing_environments = session.scalars(
        select(Environment).where(Environment.id.in_(environment_ids))
    ).all()

    existing_ids = [env.id for env in existing_environments]
    invalid_ids = [
        env_id for env_id in environment_ids if env_id not in existing_ids
    ]

    user_db.environments = existing_environments

    session.commit()

    return existing_ids, invalid_ids
