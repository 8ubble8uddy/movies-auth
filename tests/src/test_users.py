from http import HTTPStatus

from flask_security.utils import verify_password

from apps.utils import generate_random_email, generate_random_string
from core.config import CONFIG
from models.user import User
from tests.conftest import USER_EMAIL, USER_PASSWORD


def test_register(client):
    data = {
        'email': generate_random_email(8),
        'password': generate_random_string(16),
    }

    response = client.post(f'{CONFIG.flask.url_prefix}/users', json=data)

    assert response.status_code == HTTPStatus.CREATED
    assert User.query.filter_by(email=data['email']).one().email == data['email']


def test_personal_information(client, user_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['access_token'])}

    response = client.get(f'{CONFIG.flask.url_prefix}/users', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['email'] == USER_EMAIL


def test_change_password(client, user_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['access_token'])}
    body = {'old_password': USER_PASSWORD, 'new_password': generate_random_string(8)}

    response = client.put(f'{CONFIG.flask.url_prefix}/users', headers=headers, json=body)

    assert response.status_code == HTTPStatus.OK
    assert verify_password(body['new_password'], User.query.first().password)
