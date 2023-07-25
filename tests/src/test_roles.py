from http import HTTPStatus

from apps.utils import generate_random_string
from core.config import CONFIG
from models.role import Role


def test_create_role(client, admin_tokens):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}
    body = {'name': generate_random_string(8)}

    response = client.post(f'{CONFIG.flask.url_prefix}/roles', headers=headers, json=body)

    assert response.status_code == HTTPStatus.CREATED
    assert Role.query.filter_by(name=body['name']).one().name == body['name']


def test_list_roles(client, user, admin):
    roles = user.roles + admin.roles

    response = client.get(f'{CONFIG.flask.url_prefix}/roles')

    assert response.status_code == HTTPStatus.OK
    assert len(response.get_json()) == len(roles)


def test_retrieve_role(client, new_role):
    role_name = new_role.name

    response = client.get(f'{CONFIG.flask.url_prefix}/roles/{role_name}')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'name': role_name, 'description': new_role.description}


def test_update_role(client, admin_tokens, new_role):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}
    body = {'description': generate_random_string(16)}

    response = client.put(f'{CONFIG.flask.url_prefix}/roles/{new_role.name}', headers=headers, json=body)

    assert response.status_code == HTTPStatus.OK
    assert Role.query.filter_by(name=new_role.name).one().description == body['description']


def test_delete_role(client, admin_tokens, new_role):
    headers = {'Authorization': 'Bearer {token}'.format(token=admin_tokens['access_token'])}

    response = client.delete(f'{CONFIG.flask.url_prefix}/roles/{new_role.name}', headers=headers)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Role.query.filter_by(name=new_role.name).first()
