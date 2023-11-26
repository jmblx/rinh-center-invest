from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.my_type_notation import added_at, intpk


class Request(Base):
    __tablename__ = "request"
    # Модель для базы данных заявки на кредит

    id: Mapped[intpk]
    month: Mapped[int]
    age: Mapped[int]
    occupation: Mapped[str]
    annual_income: Mapped[int]
    monthly_inhand_salary: Mapped[int]
    num_bank_accounts: Mapped[int]
    num_credit_card: Mapped[int]
    num_of_loan: Mapped[int]
    num_credit_inquiries: Mapped[int]
    credit_history_age: Mapped[int]
    amount_invested_monthly: Mapped[int]
    payment_behaviour: Mapped[str]
    monthly_balance: Mapped[int]
    created_at: Mapped[added_at]
    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship(
        "User",
        back_populates="requests",
        uselist=False,
    )
    is_good_client: Mapped[float] = mapped_column(
        nullable=True
    )

