from enum import Enum


class AuthRoles(Enum):
    """Класс с перечислением ролей пользователей."""

    USER = 'user'
    SUBSCRIBER = 'subscriber'
    ADMIN = 'admin'


class OAuthProviders(Enum):
    """Класс с перечислением провайдеров OAuth."""

    YANDEX = 'yandex'
    VK = 'vk'
