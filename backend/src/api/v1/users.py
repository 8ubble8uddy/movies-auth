from http import HTTPStatus
from typing import Dict, List, Tuple
from uuid import UUID

from flask import Blueprint, make_response
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import get_current_user, get_jwt_identity, jwt_required
from werkzeug import Response
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from api.schemas import ChangePasswordSchema, RoleSchema, UserSchema
from apps.security import user_datastore as postgres
from core.decorators import admin_required
from core.enums import AuthRoles
from models.role import Role

users = Blueprint('users', __name__)


class UserView(MethodResource):
    """Класс для представления пользователя."""

    @property
    def user_role(self) -> Role:
        """Начальная роль пользователя при регистрации.

        Returns:
            Role: Роль пользователя
        """
        return postgres.find_or_create_role(AuthRoles.USER.value)

    @use_kwargs(UserSchema)
    def post(self, **kwargs) -> Response:
        """Регистрация пользователя.

        Args:
            kwargs: Параметры в теле запросе

        Raises:
            BadRequest: Ошибка, что такой пользователь уже есть

        Returns:
            Response: Ответ с кодом 201
        """
        if postgres.find_user(email=kwargs['email']):
            raise BadRequest('Пользователь с такой почтой уже есть!')
        new_user = postgres.create_user(**kwargs)
        postgres.add_role_to_user(new_user, self.user_role)
        postgres.commit()
        return make_response('', HTTPStatus.CREATED)

    @jwt_required()
    @marshal_with(UserSchema)
    def get(self) -> Tuple[Dict, int]:
        """Получение персональных данных.

        Returns:
            Tuple[Dict, int]: Личная информация и код 200
        """
        return get_current_user(), HTTPStatus.OK

    @jwt_required()
    @use_kwargs(ChangePasswordSchema)
    def put(self, **kwargs) -> Response:
        """Изменения пароля.

        Args:
            kwargs: Параметры в теле запросе

        Raises:
            Unauthorized: Ошибка, что переданы неверные данные для аутентификации пользователя

        Returns:
            Response: Ответ с кодом 200
        """
        email, password = get_jwt_identity(), kwargs['old_password']
        if not (user := postgres.authenticate_user(email, password)):
            raise Unauthorized('Не удалось аутентифицировать пользователя!')
        user.password = kwargs['new_password']
        postgres.put(user)
        postgres.commit()
        return make_response('', HTTPStatus.OK)


class SubscribeView(MethodResource):
    """Класс для представления выдачи роли подписчика по ID пользователя."""

    @property
    def subscriber_role(self) -> Role:
        """Роль подписчика, которая дает привилегии пользователю.

        Returns:
            Role: Роль подписчика
        """
        return postgres.find_or_create_role(AuthRoles.SUBSCRIBER.value)

    @admin_required
    def post(self, user_pk: UUID) -> Response:
        """Назначение пользователю роли подписчика.

        Args:
            user_pk: ID пользователя

        Raises:
            NotFound: Ошибка, что в базе данных нет такого пользователя

        Returns:
            Response: Ответ с кодом 201
        """
        if not (user := postgres.get_user(user_pk)):
            raise NotFound('Не удалось найти пользователя!')
        postgres.add_role_to_user(user, self.subscriber_role)
        postgres.commit()
        return make_response('', HTTPStatus.CREATED)

    @admin_required
    @marshal_with(RoleSchema(many=True))
    def get(self, user_pk: UUID) -> Tuple[List, int]:
        """Получение ролей у пользователя.

        Args:
            user_pk: ID пользователя

        Raises:
            NotFound: Ошибка, что в базе данных нет такого пользователя

        Returns:
            Tuple[list, int]: Список ролей пользователя и код 200
        """
        if not (user := postgres.get_user(user_pk)):
            raise NotFound('Не удалось найти пользователя!')
        return user.roles, HTTPStatus.OK

    @admin_required
    def delete(self, user_pk: UUID) -> Response:
        """Отбирание у пользователя роли подписчика.

        Args:
            user_pk: ID пользователя

        Raises:
            NotFound: Ошибка, что в базе данных нет такого пользователя

        Returns:
            Response: Ответ с кодом 204
        """
        if not (user := postgres.get_user(user_pk)):
            raise NotFound('Не удалось найти пользователя!')
        postgres.remove_role_from_user(user, self.subscriber_role)
        postgres.commit()
        return make_response('', HTTPStatus.NO_CONTENT)
