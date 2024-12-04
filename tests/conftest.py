from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from web_backend.app import app
from web_backend.database import get_session
from web_backend.models import Admin, table_registry
from web_backend.security import get_password_hash


@pytest.fixture(scope='session')
def engine() -> Generator:
    with PostgresContainer(image='postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine) -> Generator[Session, None, None]:
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    def get_session_test():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_test
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def admin(session: Session) -> Generator[Admin, None, None]:
    admin = Admin(
        email='admin_teste@example.com',
        password=get_password_hash('admin_teste1234'),
        super_admin=False,
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin


@pytest.fixture
def super_admin(session: Session) -> Generator[Admin, None, None]:
    password = 'admin_teste1234'
    super_admin = Admin(
        email='admin_teste@example.com',
        password=get_password_hash(password),
        super_admin=True,
    )

    session.add(super_admin)
    session.commit()
    session.refresh(super_admin)

    super_admin.clean_password = password

    return super_admin


@pytest.fixture
def token(client, super_admin: Admin) -> str:
    response = client.post(
        '/auth/token',
        data={
            'username': super_admin.email,
            'password': super_admin.clean_password,
        },
    )

    return response.json()['access_token']
