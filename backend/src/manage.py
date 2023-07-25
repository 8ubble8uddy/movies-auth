import logging

import flask_migrate
from flask import Flask, g, request
from flask_script import Command, Manager, prompt
from logstash import LogstashHandler

from apps import api, db, jaeger, jwt, limiter, oauth, security
from apps.security import user_datastore as postgres
from core.config import CONFIG


class RequestIdFilter(logging.Filter):
    """Класс дополнительного фильтра сообщений лога для добавления к ним информации об ID запроса."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Основной метод для добавлении в лог информации.

        Args:
            record: Обрабатываемая запись

        Returns:
            bool: Не нулевое значение для регистрации записи
        """
        record.request_id = request.headers.get('X-Request-Id', g.request_id)
        return True


def create_app() -> Flask:
    """Инициализация приложения.

    Returns:
        Flask: Приложение
    """
    app = Flask(__name__)
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    app.logger.addFilter(RequestIdFilter())
    app.logger.addHandler(LogstashHandler(CONFIG.logstash.host, CONFIG.logstash.port, version=1))
    db.install(app)
    jwt.install(app)
    security.install(app)
    api.install(app)
    oauth.install(app)
    limiter.install(app)
    jaeger.install(app)
    return app


class MakeMigrations(Command):
    """Команда для формирования миграций."""

    def run(self):
        """Скрипт запуска команды."""
        flask_migrate.migrate()


class Migrate(Command):
    """Команда для применения миграций."""

    def run(self):
        """Скрипт запуска команды."""
        flask_migrate.upgrade()


class CreateSuperUser(Command):
    """Команда для создания суперпользователя."""

    def run(self):
        """Скрипт запуска команды."""
        admin = postgres.create_user(
            email=prompt('Введите email'),
            password=prompt('Введите пароль'),
        )
        role = postgres.find_or_create_role(CONFIG.roles.ADMIN.value)
        postgres.add_role_to_user(admin, role)
        postgres.commit()


if __name__ == '__main__':
    manager = Manager(app=create_app())
    manager.add_command('makemigrations', MakeMigrations())
    manager.add_command('migrate', Migrate())
    manager.add_command('createsuperuser', CreateSuperUser())
    manager.run()
