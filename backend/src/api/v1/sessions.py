from http import HTTPStatus
from typing import Dict, List, Optional, Tuple

from flask import Blueprint, current_app, make_response, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import get_current_user, get_jwt, jwt_required
from werkzeug import Response
from werkzeug.exceptions import BadRequest, Unauthorized

from api import schemas
from apps.jwt import generate_tokens
from apps.jwt import jwt_redis_blocklist as redis
from apps.oauth import OAuthSignIn
from apps.security import user_datastore as postgres
from core.config import CONFIG

sessions = Blueprint('sessions', __name__)


class SessionView(MethodResource):
    """Класс для представления сессии пользователя."""

    @use_kwargs(schemas.UserSchema)
    @marshal_with(schemas.TokenSchema)
    def post(self, **kwargs) -> Tuple[Dict, int]:
        """Вход пользователя в аккаунт.

        Args:
            kwargs: Параметры в теле запроса

        Raises:
            Unauthorized: Ошибка, что переданы неверные данные для аутентификации пользователя

        Returns:
            tuple[dict, int]: Токены и код 201
        """
        if not (user := postgres.authenticate_user(**kwargs)):
            raise Unauthorized('Не удалось аутентифицировать пользователя!')
        postgres.create_session(user, request.user_agent)
        postgres.commit()
        return generate_tokens(user), HTTPStatus.CREATED

    @jwt_required()
    @use_kwargs(schemas.PageSchema, location='query')
    @marshal_with(schemas.SessionSchema(many=True))
    def get(self, **kwargs) -> Tuple[List, int]:
        """Получение пользователем своей истории входов в аккаунт.

        Args:
            kwargs: Параметры в строке запроса

        Returns:
            tuple[list, int]: История входов в аккаунт и код 200
        """
        user = get_current_user()
        auth_history = user.sessions.paginate(error_out=False, **kwargs)
        return auth_history.items, HTTPStatus.OK

    @jwt_required(refresh=True)
    @marshal_with(schemas.TokenSchema)
    def put(self) -> Tuple[Dict, int]:
        """Обновление access-токена.

        Returns:
            tuple[dict, int]: Токены и код 201
        """
        user = get_current_user()
        return generate_tokens(user), HTTPStatus.OK

    @jwt_required()
    def delete(self) -> Response:
        """Выход пользователя из аккаунта.

        Returns:
            Response: Ответ с кодом 204
        """
        revoked_token = get_jwt()['jti']
        redis.set(revoked_token, value='', ex=CONFIG.flask.access_token_expires_by_sec)
        return make_response('', HTTPStatus.NO_CONTENT)


class SessionByOAuth(MethodResource):
    """Класс для представления аутентификации пользователя через социальные сервисы."""

    def post(self, provider_name: str) -> Response:
        """Инициирование аутентификации через OAuth.

        Args:
            provider_name: Название провайдера OAuth

        Raises:
            BadRequest: Ошибка, что провайдера нет в конфигурации или не указаны данные для подключения к нему

        Returns:
            Response: Ответ в виде аутентификации на сайте провайдера с кодом переадресации 302
        """
        provider: Optional[OAuthSignIn] = current_app.config['OAUTH_PROVIDERS'].get(provider_name)
        if not provider:
            raise BadRequest(f'Провайдер {provider_name} не поддерживается!')
        if not (provider.service.client_id and provider.service.client_secret):
            raise BadRequest(f'Технические проблемы при подключении к провайдеру {provider_name}!')
        return provider.authorize()

    @use_kwargs(schemas.OAuthSchema, location='query')
    @marshal_with(schemas.TokenSchema)
    def get(self, provider_name: str, **kwargs) -> Tuple[Dict, int]:
        """Завершение аутентификации через OAuth.

        Args:
            provider_name: Название провайдера OAuth
            kwargs: Параметры в строке запроса

        Returns:
            tuple[dict, int]: Токены и код 201
        """
        provider: OAuthSignIn = current_app.config['OAUTH_PROVIDERS'].get(provider_name)
        social_id = provider.callback(**kwargs)
        user = postgres.find_or_create_user(social_id, provider.service.name)
        postgres.create_session(user, request.user_agent)
        postgres.commit()
        return generate_tokens(user), HTTPStatus.CREATED
