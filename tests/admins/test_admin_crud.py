from http import HTTPStatus

from fastapi.testclient import TestClient

from web_backend.models import Admin
from web_backend.schemas import AdminPublic


def test_create_admin(client: TestClient, super_admin: Admin, token: str):
    new_admin = {
        'email': 'admin_teste@example.com',
        'password': 'admin_teste1234',
        'super_admin': False,
    }

    response = client.post(
        '/admins/',
        json=new_admin,
    )

    assert response.status_code == HTTPStatus.CREATED
    admin: AdminPublic = response.json()

    assert 'id' in admin
    assert admin.email == new_admin['email']
    assert admin.super_admin == new_admin['super_admin']


# def test_create_user_username_already_exist(client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': f'{user.username}',
#             'email': 'test@test.com',
#             'password': 'testtest',
#         },
#     )

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'Username already exists'}


# def test_create_user_email_already_exist(client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': 'test',
#             'email': f'{user.email}',
#             'password': 'testtest',
#         },
#     )

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'Email already exists'}


# def test_create_user_username_and_email_already_exist(client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': f'{user.username}',
#             'email': f'{user.email}',
#             'password': 'testtest',
#         },
#     )

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'Username and email already exists'}


# def test_delete_user(client, user, token):
#     response = client.delete(
#         f'/users/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'User deleted successfully'}


# def test_delete_user_forbidden(client, other_user, token):
#     response = client.delete(
#         f'/users/{other_user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Not enough permissions'}


# def test_read_users(client, user):
#     user_public = UserPublicSchema.model_validate(user).model_dump()
#     response = client.get('/users/')

#     assert response.status_code == HTTPStatus.OK
#     user_public['created_at'] = user_public['created_at'].isoformat()
#     user_public['updated_at'] = user_public['updated_at'].isoformat()
#     assert response.json() == {'users': [user_public]}


# def test_update_user(client, user, token):
#     update_data = {
#         'username': 'updated_username',
#         'email': 'updated_email@example.com',
#         'password': 'new_password',
#         'status': 'active',
#     }

#     response = client.put(
#         f'/users/{user.id}',
#         json=update_data,
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     assert response.status_code == HTTPStatus.OK
#     updated_user = response.json()
#     assert updated_user['username'] == update_data['username']
#     assert updated_user['email'] == update_data['email']


# def test_update_user_forbidden(client, other_user, token):
#     response = client.put(
#         f'/users/{other_user.id}',
#         json={
#             'username': 'teste_com_put',
#             'email': 'teste_put@put.com',
#             'password': 'teste_senha_put',
#         },
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Not enough permissions'}
