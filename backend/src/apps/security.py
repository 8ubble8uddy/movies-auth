from typing import Optional

from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import verify_password
from sqlalchemy import and_
from werkzeug.user_agent import UserAgent

from apps.db import db
from apps.utils import generate_random_email, generate_random_string
from core.config import CONFIG
from models.role import Role
from models.session import Session
from models.user import SocialAccount, User


class CustomUserDatastore(SQLAlchemyUserDatastore):
    """Класс для работы с базой данных пользователей."""

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Аутентифицирует и возвращает пользователя, если переданы верные данные.

        Args:
            email: Почта
            password: Пароль

        Returns:
            Optional[User]: Пользователь после аутентификации или None, если не прошел проверку
        """
        user = self.find_user(email=email)
        return user if user and verify_password(password, user.password) else None

    def create_session(self, user: User, user_agent: UserAgent) -> Session:
        """Создает и возвращает новую сессию пользователю.

        Args:
            user: Пользователь
            user_agent: Объект с данными `User-Agent`

        Returns:
            Session: Сессия пользователя
        """
        session = Session(user_pk=user.pk, user_agent=user_agent.string, user_device_type=user_agent)
        return self.put(session)

    def create_social_account(self, user: User, social_id: str, social_name: str) -> SocialAccount:
        """Создание социального аккаунта у пользователя.

        Args:
            user: Пользователь
            social_id: ID пользователя в социальном сервисе
            social_name: Название социального сервиса

        Returns:
            SocialAccount: Социальный аккаунт пользователя
        """
        social = SocialAccount(user_pk=user.pk, social_id=social_id, social_name=social_name)
        return self.put(social)

    def find_social_account(self, social_id: str, social_name: str) -> Optional[SocialAccount]:
        """Поиск социального аккаунта по заданным параметрам.

        Args:
            social_id: ID пользователя в социальном сервисе
            social_name: Название социального сервиса

        Returns:
            Optional[SocialAccount]: Социальный аккаунт или None, если ничего не нашли
        """
        query = SocialAccount.query.filter(
            and_(SocialAccount.social_id == social_id, SocialAccount.social_name == social_name),
        )
        return query.first()

    def find_or_create_user(self, social_id: str, social_name: str) -> User:
        """Поиск или создание пользователя по ID в социальном сервисе.

        Args:
            social_id: ID пользователя в социальном сервисе
            social_name: Название социального сервиса

        Returns:
            User: Пользователь с идентификацией по его ID в социальном сервисе
        """
        social_account = self.find_social_account(social_id, social_name)
        if not social_account:
            user = self.create_user(email=generate_random_email(8), password=generate_random_string(16))
            social_account = self.create_social_account(user, social_id, social_name)
            user.social_accounts.append(social_account)
            self.put(user)
            self.commit()
        return social_account.user


security = Security()
user_datastore = CustomUserDatastore(db, User, Role)


def install(app: Flask):
    """Установка компонента Flask для работы с хранилищем данных пользователей.

    Args:
        app: Flask
    """
    app.config['SECURITY_PASSWORD_SALT'] = CONFIG.flask.password_salt
    security.init_app(app, user_datastore)
