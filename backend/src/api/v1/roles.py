from http import HTTPStatus
from typing import Dict, List, Tuple

from flask import Blueprint, make_response
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from werkzeug import Response
from werkzeug.exceptions import BadRequest, NotFound

from api.schemas import RoleSchema
from apps.security import user_datastore as postgres
from core.decorators import admin_required

roles = Blueprint('roles', __name__)


class RoleView(MethodResource):
    """Класс для представлений ролей."""

    @admin_required
    @use_kwargs(RoleSchema)
    def post(self, **kwargs) -> Response:
        """Создание роли.

        Args:
            kwargs: Параметры в теле запросе

        Raises:
            BadRequest: Ошибка, что такая роль уже есть

        Returns:
            Response: Ответ с кодом 201
        """
        if postgres.find_role(kwargs['name']):
            raise BadRequest('Роль c таким названием уже есть!')
        postgres.create_role(**kwargs)
        postgres.commit()
        return make_response('', HTTPStatus.CREATED)

    @marshal_with(RoleSchema(many=True))
    def get(self) -> Tuple[List, int]:
        """Получение списка ролей.

        Returns:
            tuple[list, int]: Список ролей и код 200
        """
        roles_list = postgres.role_model.query.all()
        return roles_list, HTTPStatus.OK


class RoleByNameView(MethodResource):
    """Класс для представления роли по названию."""

    @marshal_with(RoleSchema)
    def get(self, role_name: str) -> Tuple[Dict, int]:
        """Получение роли по названию.

        Args:
            role_name: Название

        Raises:
            NotFound: Ошибка, что в базе данных нет такой роли

        Returns:
            tuple[dict, int]: Роль и код 200
        """
        if not (role := postgres.find_role(role_name)):
            raise NotFound('Не удалось найти роль!')
        return role, HTTPStatus.OK

    @admin_required
    @use_kwargs(RoleSchema(partial=['name']))
    def put(self, role_name: str, **kwargs) -> Response:
        """Изменение роли по заданным параметрам.

        Args:
            role_name: Название
            kwargs: Параметры в теле запросе

        Raises:
            NotFound: Ошибка, что в базе данных нет такой роли

        Returns:
            Response: Ответ с кодом 200
        """
        if not (role := postgres.find_role(role_name)):
            raise NotFound('Не удалось найти роль!')
        for field, value in kwargs.items():
            setattr(role, field, value)
        postgres.put(role)
        postgres.commit()
        return make_response('', HTTPStatus.OK)

    @admin_required
    def delete(self, role_name: str) -> Response:
        """Удаление роли.

        Args:
            role_name: Название

        Raises:
            NotFound: Ошибка, что в базе данных нет такой роли

        Returns:
            Response: Ответ с кодом 204
        """
        if not (role := postgres.find_role(role_name)):
            raise NotFound('Не удалось найти роль!')
        postgres.delete(role)
        postgres.commit()
        return make_response('', HTTPStatus.NO_CONTENT)
