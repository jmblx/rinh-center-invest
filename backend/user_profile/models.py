import uuid
from typing import List

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.my_type_notation import added_at, intpk
from src.processing_appeals.models import Message


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[JSON] = mapped_column(JSON)
    user: Mapped["User"] = relationship(back_populates="roles", uselist=False)


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    @staticmethod
    def default_username(context):
        return str(context.get_current_parameters()["email"].split("@")[0])

    @staticmethod
    def default_competencies_count(context):
        competencies = context.get_current_parameters()["competencies"]
        count_of_competencies = sum(value for value in competencies.values())
        return count_of_competencies

    @staticmethod
    def default_tasks_count(context):
        return 0 if context.get_current_parameters()["role_id"] == 1 else None

    email: Mapped[str]
    username: Mapped[str] = mapped_column(default=default_username)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=2)
    roles: Mapped[list["Role"]] = relationship(
        back_populates="user", uselist=True
    )
    competencies: Mapped[JSON] = mapped_column(JSON, nullable=True, default={})
    competencies_count: Mapped[int] = mapped_column(
        onupdate=default_competencies_count, nullable=True
    )
    tasks_count: Mapped[int] = mapped_column(
        nullable=True, default=default_tasks_count
    )
    messages: Mapped["Message"] = relationship(
        back_populates="author", uselist=True
    )
    registered_at: Mapped[added_at]
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=True)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
