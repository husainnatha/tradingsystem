from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey
)

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)

    broker = Column(String, nullable=False)

    account_name = Column(String, nullable=False)

    currency = Column(String, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)

    transaction_hash = Column(String, unique=True, 
                              nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )
    
    trade_date = Column(Date, nullable=False)

    symbol = Column(String, nullable=False)

    action = Column(String, nullable=False)

    quantity = Column(Float, nullable=False)

    trade_currency = Column(String, nullable=False)

    trade_price = Column(Float, nullable=False)

    fees = Column(Float, default=0)

    fx_rate_to_gbp = Column(Float, nullable=False)

    gbp_net_amount = Column(Float, nullable=False)

    notes = Column(String)