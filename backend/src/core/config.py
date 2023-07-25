from functools import lru_cache

from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):
    """Класс с настройками подключения к PostgreSQL."""

    host: str = '127.0.0.1'
    port: int = 5432
    db: str = 'users_database'
    user: str = 'postgres'
    password: str = 'postgres'


class RedisConfig(BaseSettings):
    """Класс с настройками подключения к Redis."""

    host: str = '127.0.0.1'
    port: int = 6379


class FlaskConfig(BaseSettings):
    """Класс с настройками подключения к FastAPI."""

    host: str = '0.0.0.0'
    port: int = 5000
    docs: str = 'openapi'
    project_name: str = 'Cервис авторизации для онлайн-кинотеатра'
    url_prefix: str = '/api/v1'
    access_token_expires_by_sec: int = 60 * 60
    secret_key: str = 'secret_key'
    password_salt: str = ''
    date_format: str = '%d/%m/%Y %H:%M:%S'


class OAuthConfig(BaseSettings):
    """Класс с настройками для подключения к провайдеру OAuth."""

    id: str = ''
    secret: str = ''


class JaegerConfig(BaseSettings):
    """Класс с настройками для распределённой трассировки запросов."""

    host: str = '127.0.0.1'
    port: int = 6831
    enabled: bool = False


class LogstashConfig(BaseSettings):
    """Класс с настройками подключения к Logstash."""

    host: str = '127.0.0.1'
    port: int = 5044


class MainSettings(BaseSettings):
    """Класс с основными настройками проекта."""

    flask: FlaskConfig = Field(default_factory=FlaskConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    yandex: OAuthConfig = Field(default_factory=OAuthConfig)
    vk: OAuthConfig = Field(default_factory=OAuthConfig)
    jaeger: JaegerConfig = Field(default_factory=JaegerConfig)
    logstash: LogstashConfig = Field(default_factory=LogstashConfig)


@lru_cache()
def get_settings() -> MainSettings:
    """
    Функция для создания объекта настроек в едином экземпляре (синглтона).

    Returns:
        MainSettings: Объект с настройками
    """
    return MainSettings(_env_file='.env', _env_nested_delimiter='_')  # type: ignore[call-arg]


CONFIG = get_settings()
