import enum
from typing import List

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.my_type_notation import added_at, intpk


class Priority(enum.Enum):
    standart = "standart priority"
    medium = "medium priority"
    high = "high priority"


class Tone(enum.Enum):
    neutral = "neutral"
    positive = "positive"
    negative = "negative"


class Message(Base):
    __tablename__ = "message"

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(TEXT)
    category: Mapped["Category"] = relationship(
        back_populates="messages", uselist=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), nullable=True
    )
    time_added: Mapped[added_at]
    author = relationship("User", back_populates="messages", uselist=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    priority: Mapped[Priority]


class Category(Base):
    __tablename__ = "category"

    id: Mapped[intpk]
    name: Mapped[str]
    messages: Mapped[List["Message"]] = relationship(
        back_populates="category",
        uselist=True,
    )


class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    chat_id: Mapped[int] = mapped_column(nullable=True)
    is_finished: Mapped[bool] = mapped_column(default=False)
    responding_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
