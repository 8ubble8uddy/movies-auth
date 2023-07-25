from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from redis import Redis

from apps.security import user_datastore as postgres
from core.config import CONFIG
from models.user import User


class AccessToken:
    """Токен для получения доступа к ресурсам."""

    def __init__(self, user: User):
        """При инициализации генерирует пользователю токен.

        Args:
            user: Пользователь
        """
        self.access_token = create_access_token(
            identity=user.email,
            additional_claims={
                'roles': [role.name for role in user.roles],
                'user_id': user.pk,
            },
        )


class RefreshToken:
    """Токен для получения новых токенов взамен старых."""

    def __init__(self, user: User):
        """При инициализации генерирует пользователю токен.

        Args:
            user: Пользователь
        """
        self.refresh_token = create_refresh_token(
            identity=user.email,
            additional_claims={
                'roles': [role.name for role in user.roles],
                'user_id': user.pk,
            },
        )


def generate_tokens(user: User) -> dict:
    """Генерирует пару ключей пользователя.

    Args:
        user: Пользователь

    Returns:
        dict: Ключ для доступа и ключ для обновления
    """
    return {**AccessToken(user).__dict__, **RefreshToken(user).__dict__}


jwt = JWTManager()
jwt_redis_blocklist = Redis(host=CONFIG.redis.host, port=CONFIG.redis.port)


def install(app: Flask):
    """Установка компонента Flask для работы с JWT токенами.

    Args:
        app: Flask
    """
    app.config['SECRET_KEY'] = CONFIG.flask.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = CONFIG.flask.access_token_expires_by_sec
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload['jti']
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_data):
        email = jwt_data['sub']
        return postgres.find_user(email=email)
