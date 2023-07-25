from marshmallow import Schema, fields, validate

from core.config import CONFIG


class UserSchema(Schema):
    """Схема для валидации пользователя."""

    email = fields.Email(required=True, validate=[validate.Length(max=250)])
    password = fields.String(required=True, validate=[validate.Length(min=8, max=100)], load_only=True)
    roles = fields.List(fields.String, dump_only=True)


class ChangePasswordSchema(Schema):
    """Схема для валидации формы изменения пароля."""

    old_password = fields.String(required=True, load_only=True)
    new_password = fields.String(required=True, validate=[validate.Length(min=8, max=100)], load_only=True)


class TokenSchema(Schema):
    """Схема для валидации выдачи токенов."""

    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)


class RoleSchema(Schema):
    """Схема для валидации роли."""

    name = fields.String(required=True, validate=[validate.Length(max=80)])
    description = fields.String(validate=[validate.Length(max=255)])


class SessionSchema(Schema):
    """Схема для валидации сессии."""

    event_date = fields.DateTime(format=CONFIG.flask.date_format, dump_only=True)
    user_agent = fields.String(dump_only=True)


class PageSchema(Schema):
    """Схема для валидации страницы."""

    page = fields.Integer(data_key='page_number', validate=[validate.Range(min=1)], load_only=True)
    per_page = fields.Integer(data_key='page_size', validate=[validate.Range(max=100)], load_only=True)


class OAuthSchema(Schema):
    """Схема для валидации ответа от провайдера OAuth."""

    code = fields.String(required=True, load_only=True)
