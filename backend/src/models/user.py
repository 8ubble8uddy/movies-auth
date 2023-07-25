import uuid

from flask_security.utils import hash_password
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from apps.db import db
from models.role import roles_users


class User(db.Model):  # type: ignore[name-defined]
    """Модель пользователя."""

    __tablename__ = 'users'

    pk = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email = db.Column(
        db.String(255),
        unique=True,
        index=True,
    )
    password = db.Column(
        db.String(255),
    )
    active = db.Column(
        db.Boolean(),
    )
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    sessions = db.relationship(
        'Session',
        backref=db.backref('user', lazy='joined'),
        lazy='dynamic',
        order_by='Session.event_date.desc()',
        passive_deletes=True,
    )

    @validates('password')
    def validate_password(self, key: str, value: str) -> str:
        """Хеширует переданный пароль.

        Args:
            key: Названиие поля
            value: Пароль

        Returns:
            str: Пароль в виде хэша
        """
        return hash_password(value)


class SocialAccount(db.Model):  # type: ignore[name-defined]
    """Модель социального аккаунта пользователя."""

    __tablename__ = 'social_account'

    pk = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_pk = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.pk', ondelete='CASCADE'),
        nullable=False,
    )
    user = db.relationship(
        User,
        backref=db.backref('social_accounts', lazy=True),
    )
    social_id = db.Column(
        db.Text,
        nullable=False,
    )
    social_name = db.Column(
        db.Text,
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint('social_id', 'social_name', name='social_pk'),
    )
