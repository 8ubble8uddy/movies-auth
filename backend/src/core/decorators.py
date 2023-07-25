from functools import wraps
from typing import Callable

from flask_jwt_extended import get_jwt, verify_jwt_in_request
from werkzeug.exceptions import Forbidden

from core.enums import AuthRoles


def admin_required(view: Callable) -> Callable:
    """
    Декоратор для доступа к ресурсу только админам.

    Args:
        view: Функция для представления ресурса

    Returns:
        Callable: Декорируемая функция
    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if AuthRoles.ADMIN.value not in claims['roles']:
            raise Forbidden('Доступно только для админов')
        return view(*args, **kwargs)
    return wrapper
