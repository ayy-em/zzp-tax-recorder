from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Numeric, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class TransactionCategory(str, Enum):
    GENERAL = "general"
    
    # Income categories
    SALARY = "salary"
    CONSULTING = "consulting"
    PROJECT = "project"
    OTHER_INCOME = "other_income"
    
    # Expense categories
    OFFICE = "office"
    TRAVEL = "travel"
    TRANSPORTATION = "transportation"
    SOFTWARE_AND_LICENSES = "software_and_licenses"
    MARKETING = "marketing"
    PROFESSIONAL_SERVICES = "professional_services"
    TAXES = "taxes"
    IT_INFRASTRUCTURE = "it_infrastructure"
    WEB_HOSTING = "web_hosting"
    SALARIES = "salaries"
    OTHER_EXPENSE = "other_expense"

class Transaction(Base):
    """Base class for both Income and Expense transactions"""
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    year: Mapped[int] = mapped_column(Integer, default=lambda: datetime.now().year)
    description: Mapped[str] = mapped_column(String(500))
    counterparty: Mapped[str] = mapped_column(String(200))  # Company or person name
    net_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    vat_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    type: Mapped[TransactionType] = mapped_column(default=TransactionType.EXPENSE)
    category: Mapped[TransactionCategory] = mapped_column(default=TransactionCategory.GENERAL)
    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.PENDING)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "transaction"
    }

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id!r}, type={self.type!r}, amount={self.gross_amount!r})>"

class Income(Transaction):
    """Income transaction model"""
    __tablename__ = "incomes"
    
    id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": TransactionType.INCOME
    }

class Expense(Transaction):
    """Expense transaction model"""
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": TransactionType.EXPENSE
    }
