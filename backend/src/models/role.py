import uuid

from sqlalchemy.dialects.postgresql import UUID

from apps.db import db


class Role(db.Model):  # type: ignore[name-defined]
    """Модель роли пользователя."""

    __tablename__ = 'roles'

    pk = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = db.Column(
        db.String(80),
        unique=True,
    )
    description = db.Column(
        db.String(255),
    )

    def __repr__(self) -> str:
        """
        Представление роли в виде названия.

        Returns:
            str: Название роли
        """
        return self.name.title()


roles_users = db.Table(
    'roles_users',
    db.Column(
        'user_pk',
        UUID(as_uuid=True),
        db.ForeignKey('users.pk', ondelete='CASCADE'),
        nullable=False,
    ),
    db.Column(
        'role_pk',
        UUID(as_uuid=True),
        db.ForeignKey('roles.pk', ondelete='CASCADE'),
        nullable=False,
    ),
)
