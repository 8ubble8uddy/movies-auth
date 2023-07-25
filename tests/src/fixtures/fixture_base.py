import pytest

from manage import create_app
from apps.db import db
from sqlalchemy.orm.session import close_all_sessions


@pytest.fixture
def app():
    app = create_app()
    app.app_context().push()
    db.create_all()
    yield app
    close_all_sessions()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
