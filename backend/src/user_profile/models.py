from typing import List

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.my_type_notation import added_at
from src.processing_credit.models import Request


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    email: Mapped[str]
    registered_at: Mapped[added_at]
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=True)
    requests: Mapped[List["Request"]] = relationship(
        back_populates="user",
        uselist=True,
    )
