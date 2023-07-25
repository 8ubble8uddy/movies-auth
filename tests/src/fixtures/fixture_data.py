import pytest

from apps.security import user_datastore as postgres
from core.config import CONFIG
from core.enums import AuthRoles
from tests import conftest as test


@pytest.fixture
def user():
    user = postgres.create_user(
        pk=test.USER_ID,
        email=test.USER_EMAIL,
        password=test.USER_PASSWORD,
    )
    role = postgres.find_or_create_role(AuthRoles.USER.value)
    postgres.add_role_to_user(user, role)
    postgres.commit()
    return user


@pytest.fixture
def user_tokens(client, user):
    data = {'email': user.email, 'password': test.USER_PASSWORD}
    response = client.post(f'{CONFIG.flask.url_prefix}/sessions', json=data)
    return response.get_json()


@pytest.fixture
def user_subscriber(user):
    role = postgres.find_or_create_role(AuthRoles.SUBSCRIBER.value)
    postgres.add_role_to_user(user, role)
    postgres.commit()
    return user


@pytest.fixture
def admin():
    admin = postgres.create_user(
        email=test.ADMIN_EMAIL,
        password=test.ADMIN_PASSWORD,
    )
    role = postgres.find_or_create_role(AuthRoles.ADMIN.value)
    postgres.add_role_to_user(admin, role)
    postgres.commit()
    return admin


@pytest.fixture
def admin_tokens(client, admin):
    data = {'email': admin.email, 'password': test.ADMIN_PASSWORD}
    response = client.post(f'{CONFIG.flask.url_prefix}/sessions', json=data)
    return response.get_json()


@pytest.fixture
def new_role():
    role = postgres.create_role(name=test.ROLE_NAME)
    postgres.commit()
    return role
