from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from web_backend.app import app
from web_backend.database import get_session
from web_backend.models import Admin, Worker, table_registry
from web_backend.security import get_password_hash


@pytest.fixture
def client(session: Session) -> Generator[TestClient, None, None]:
    def get_session_test():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_test
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine() -> Generator[Engine, None, None]:
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
def worker(session: Session) -> Worker:
    txt = 'fixture_worker'
    worker = Worker(
        name=txt,
        email=txt + '@test.com',
    )

    session.add(worker)
    session.commit()
    session.refresh(worker)

    return worker


@pytest.fixture
def token(client, admin: Admin) -> str:
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
