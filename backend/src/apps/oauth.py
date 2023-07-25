import abc

from flask import Flask, redirect, url_for
from rauth import OAuth2Service
from werkzeug import Response

from apps.utils import decode_json
from core.config import CONFIG
from core.enums import OAuthProviders


class OAuthSignIn(abc.ABC):
    """Абстрактный класс для реализации провайдера OAuth."""

    service: OAuth2Service = None

    @abc.abstractmethod
    def callback(self, code: str) -> str:
        """Завершение аутентификациии с провайдером и получения информации о пользователе.

        Args:
            code: Код авторизации для получения данных пользователя
        """

    @property
    def callback_url(self) -> str:
        """Url-адрес, на который провайдер должен перенаправить пользователя после успешной аутентификациии.

        Returns:
            str: Url-адрес для обратного вызова при аутентификациии через OAuth
        """
        return url_for('sessions.sessionbyoauth', provider_name=self.service.name, _external=True)

    def authorize(self) -> Response:
        """Перенаправление на сайт провайдера, где пользователь должен пройти аутентификациию.

        Returns:
            Response: Ответ в виде переадресации на нужный адрес
        """
        return redirect(location=self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self.callback_url,
        ))


class YandexSignIn(OAuthSignIn):
    """Класс для реализации провайдера Yandex, который реализует OAuth2."""

    def __init__(self, client_id: str, client_secret: str):
        """При инициализации требуется client_id и client_secret, которые назначены приложению в Yandex.

        Args:
            client_id: Идентификатор приложения
            client_secret: Секретный код
        """
        self.service = OAuth2Service(
            name='yandex',
            client_id=client_id,
            client_secret=client_secret,
            authorize_url='https://oauth.yandex.com/authorize',
            access_token_url='https://oauth.yandex.com/token',
            base_url='https://login.yandex.ru/',
        )

    def callback(self, code: str) -> str:
        """Метод обратного вызова после проверки подлинности данных пользователя в Yandex.

        Args:
            code: Код для доступа к данным пользователя

        Returns:
            str: ID пользователя в Yandex
        """
        data = {
            'code': code,
            'grant_type': 'authorization_code',
        }
        oauth_session = self.service.get_auth_session(data=data, decoder=decode_json)
        response = oauth_session.get('info').json()
        return response['id']


class VkSignIn(OAuthSignIn):
    """Класс для реализации провайдера VK, который реализует OAuth2."""

    def __init__(self, client_id: str, client_secret: str):
        """При инициализации требуется client_id и client_secret, которые назначены приложению в VK.

        Args:
            client_id: Идентификатор приложения
            client_secret: Секретный код
        """
        self.service = OAuth2Service(
            name='vk',
            client_id=client_id,
            client_secret=client_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://api.vk.com/method/',
        )

    def callback(self, code: str) -> str:
        """Метод обратного вызова после проверки подлинности данных пользователя в VK.

        Args:
            code: Код для доступа к данным пользователя

        Returns:
            str: ID пользователя в VK
        """
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.callback_url,
        }
        response = self.service.get_raw_access_token(data=data).json()
        return response['user_id']


def install(app: Flask):
    """Установка конфигурации приложения Flask в части подключения к пройвадерам OAuth.

    Args:
        app: Flask
    """
    app.config['OAUTH_PROVIDERS'] = {
        OAuthProviders.YANDEX.value: YandexSignIn(
            client_id=CONFIG.yandex.id,
            client_secret=CONFIG.yandex.secret,
        ),
        OAuthProviders.VK.value: VkSignIn(
            client_id=CONFIG.vk.id,
            client_secret=CONFIG.vk.secret,
        ),
    }
