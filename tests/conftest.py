import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator

from fastapi.testclient import TestClient
from web_backend.models import table_registry
from web_backend.database import get_session
from testcontainers.postgres import PostgresContainer

from web_backend.app import app

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