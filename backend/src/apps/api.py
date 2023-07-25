from http import HTTPStatus
from typing import Any, Tuple, Union

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Blueprint, Flask, jsonify
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from werkzeug import exceptions as exc
from werkzeug.wrappers import Response

from api.v1.roles import roles
from api.v1.sessions import sessions
from api.v1.users import users
from core.config import CONFIG

docs = FlaskApiSpec()


def handle_errors(error: exc.HTTPException) -> Tuple[Union[Any, Response], ...]:
    """Функция для обработки исключений.

    Args:
        error: Исключение

    Returns:
        Tuple: Обработанное исчключение с соответствующим сообщением и кодом ошибки
    """
    if error.code == HTTPStatus.UNPROCESSABLE_ENTITY:
        headers = error.get_headers()
        messages = error.description
        if headers:
            return jsonify({'message': messages}), HTTPStatus.BAD_REQUEST, headers
        return jsonify({'message': messages}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': error.description}), error.code


def path(url: str, blueprint: Blueprint, view: MethodResource):
    """Функция для регистрации URL-адреса.

    Args:
        url: URL-адрес
        blueprint: Объект `Blueprint`
        view: Класс представления
    """
    blueprint.add_url_rule(
        rule='{api_url}{path}'.format(api_url=CONFIG.flask.url_prefix, path=url),
        view_func=view.as_view(view.__name__.lower()),
        strict_slashes=False,
    )
    for error in (exc.NotFound, exc.Unauthorized, exc.Forbidden, exc.BadRequest, exc.UnprocessableEntity):
        blueprint.register_error_handler(error, handle_errors)  # type: ignore[arg-type]
    docs.register(view, blueprint=blueprint.name)


def install(app: Flask):
    """Установка компонента Flask для работы с API.

    Args:
        app: Flask
    """
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title=CONFIG.flask.project_name,
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_UI_URL': f'/{CONFIG.flask.docs}',
        'APISPEC_SWAGGER_URL': f'/{CONFIG.flask.docs}-json',
    })
    from api.urls import urlpatterns
    app.register_blueprint(roles)
    app.register_blueprint(users)
    app.register_blueprint(sessions)
    docs.init_app(app)
