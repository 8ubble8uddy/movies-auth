import json
import string
from secrets import choice


def generate_random_string(length: int) -> str:
    """Функция для генерации случайной строки.

    Args:
        length: Размер строки

    Returns:
        str: Строка со случайными буквами и цифрами
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(choice(alphabet) for _ in range(length))


def generate_random_email(length: int, domain: str = 'yandex') -> str:
    """Функция для генерации случайного адреса почты.

    Args:
        length: Размер строки в виде имени почтового ящика
        domain: Доменное имя

    Returns:
        str: Адрес почты из случайной строки и доменного имени
    """
    random_str = generate_random_string(length)
    return '{random_str}@{domain}.com'.format(random_str=random_str, domain=domain)


def decode_json(payload: bytes) -> object:
    """Функция для декодирования содержимого JSON в объект.

    Args:
        payload: Содержимое JSON в байтах

    Returns:
        object: Объект
    """
    return json.loads(payload.decode('utf-8'))
