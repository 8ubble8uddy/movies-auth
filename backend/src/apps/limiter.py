from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

rate_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['10/second'],
    strategy='moving-window',
)


def install(app):
    """Установка компонента Flask для ограничения количества запросов к серверу.

    Args:
        app: Flask
    """
    rate_limiter.init_app(app)
