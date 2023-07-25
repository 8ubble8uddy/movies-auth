from http import HTTPStatus

from api.schemas import RoleSchema
from core.config import CONFIG
from core.enums import AuthRoles


def test_add_subscription(client, user, admin_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}

    response = client.post(f'{CONFIG.flask.url_prefix}/users/{user.pk}/subscribe', headers=headers)

    assert response.status_code == HTTPStatus.CREATED
    assert AuthRoles.SUBSCRIBER.value.title() in list(map(str, user.roles))


def test_check_subscription(client, user_subscriber, admin_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}

    response = client.get(f'{CONFIG.flask.url_prefix}/users/{user_subscriber.pk}/subscribe', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == RoleSchema().dump(user_subscriber.roles, many=True)


def test_delete_subscription(client, user_subscriber, admin_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}

    response = client.delete(f'{CONFIG.flask.url_prefix}/users/{user_subscriber.pk}/subscribe', headers=headers)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert AuthRoles.SUBSCRIBER.value.title() not in list(map(str, user_subscriber.roles))
