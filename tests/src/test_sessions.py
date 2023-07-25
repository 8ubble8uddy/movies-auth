from http import HTTPStatus

from core.config import CONFIG
from models.session import Session
from tests.conftest import USER_PASSWORD


def test_login(client, user):
    body = {'email': user.email, 'password': USER_PASSWORD}

    response = client.post(f'{CONFIG.flask.url_prefix}/sessions', json=body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json().get('access_token')
    assert response.get_json().get('refresh_token')


def test_auth_history(client, user_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['access_token'])}

    response = client.get(f'{CONFIG.flask.url_prefix}/sessions', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert f'{Session.query.first().event_date:{CONFIG.flask.date_format}}' == response.get_json()[0]['event_date']


def test_update_tokens(client, user_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['refresh_token'])}

    response = client.put(f'{CONFIG.flask.url_prefix}/sessions', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json().get('access_token')
    assert response.get_json().get('refresh_token')


def test_logout(client, user_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['access_token'])}

    response = client.delete(f'{CONFIG.flask.url_prefix}/sessions', headers=headers)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert client.get(f'{CONFIG.flask.url_prefix}/users', headers=headers).status_code == HTTPStatus.UNAUTHORIZED
