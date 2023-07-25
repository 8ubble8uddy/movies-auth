from http import HTTPStatus

import pytest

from apps.utils import generate_random_string
from core.config import CONFIG
from tests.conftest import ROLE_NAME, USER_ID, USER_PASSWORD


@pytest.mark.parametrize(
    'http_method, url, body',
    [
        ('post', f'{CONFIG.flask.url_prefix}/users/{USER_ID}/subscribe', {}),
        ('get', f'{CONFIG.flask.url_prefix}/users/{USER_ID}/subscribe', {}),
        ('delete', f'{CONFIG.flask.url_prefix}/users/{USER_ID}/subscribe', {}),
    
        ('post', f'{CONFIG.flask.url_prefix}/roles', {'name': generate_random_string(8)}),
        ('put', f'{CONFIG.flask.url_prefix}/roles/{ROLE_NAME}', {'description': generate_random_string(16)}),
        ('delete', f'{CONFIG.flask.url_prefix}/roles/{ROLE_NAME}', {}),
    ]
)
def test_user_permission_denied(client, user_tokens, http_method, url, body):
    headers = {'Authorization': 'Bearer {token}'.format(token=user_tokens['access_token'])}

    response = getattr(client, http_method)(url, headers=headers, json=body)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    'http_method, url, body',
    [
        ('get', f'{CONFIG.flask.url_prefix}/users/', {}),
        ('put', f'{CONFIG.flask.url_prefix}/users/', {
            'old_password': USER_PASSWORD,
            'new_password': generate_random_string(8),
        }),
    ]
)
def test_anonymous_permission_demnied(client, user, http_method, url, body):
    response = getattr(client, http_method)(url, json=body)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
