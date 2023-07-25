import uuid

USER_EMAIL = 'testuser@mail.com'
USER_PASSWORD = 'testpassword'
USER_ID = uuid.uuid4()

ADMIN_EMAIL = 'admin@mail.ru'
ADMIN_PASSWORD = 'adminpassword'

ROLE_NAME = 'testrole'

pytest_plugins = [
    'tests.src.fixtures.fixture_base',
    'tests.src.fixtures.fixture_data',
]
