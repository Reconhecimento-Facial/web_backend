from http import HTTPStatus

from fastapi.testclient import TestClient

from web_backend.models import UserStatus
from web_backend.schemas import UserPublicSchema


def test_create_user(client: TestClient):
    user = {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test',
    }

    response = client.post(
        '/users/',
        json=user,
    )

    assert response.status_code == HTTPStatus.CREATED
    user_public: UserPublicSchema = response.json()

    assert 'id' in user_public
    assert user_public['status'] == UserStatus.disabled
    assert 'created_at' in user_public
    assert 'updated_at' in user_public
    assert user_public['username'] == user['username']
    assert user_public['email'] == user['email']


def test_create_user_username_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': f'{user.email}',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_username_and_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}',
            'email': f'{user.email}',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username and email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_forbidden(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_read_users(client, user):
    user_public = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    user_public['created_at'] = user_public['created_at'].isoformat()
    user_public['updated_at'] = user_public['updated_at'].isoformat()
    assert response.json() == {'users': [user_public]}
