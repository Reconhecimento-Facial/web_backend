from http import HTTPStatus


def test_login_for_acces_token_does_not_exist(client):
    response = client.post(
        url='/auth/token',
        data={
            'username': 'does_not_exist@example.com',
            'password': 'does_not_exist',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_for_access_token_incorrect_password(client, admin):
    response = client.post(
        url='/auth/token',
        data={
            'username': admin.email,
            'password': 'incorrect_password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
