from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import CONFIG

db = SQLAlchemy()
migrate = Migrate()


def install(app: Flask):
    """Установка компонента Flask для работы с базой данных PostgreSQL.

    Args:
        app: Flask
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            user=CONFIG.postgres.user,
            password=CONFIG.postgres.password,
            host=CONFIG.postgres.host,
            port=CONFIG.postgres.port,
            db=CONFIG.postgres.db,
        ))
    db.init_app(app)
    migrate.init_app(app, db)
