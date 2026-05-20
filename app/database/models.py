from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date
)

# -----------------------------------
# BASE MODEL
# -----------------------------------

class Base(DeclarativeBase):
    pass

# -----------------------------------
# TRANSACTIONS TABLE
# -----------------------------------

class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True
    )

    transaction_hash = Column(
        String,
        unique=True,
        nullable=False
    )

    # -----------------------------
    # IMPORT FIELDS
    # -----------------------------

    trade_date = Column(
        Date,
        nullable=False
    )

    account = Column(
        String,
        nullable=False
    )

    symbol = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    trade_currency = Column(
        String,
        nullable=False
    )

    trade_price = Column(
        Float,
        nullable=False
    )

    fees = Column(
        Float,
        default=0
    )

    fx_rate_to_gbp = Column(
        Float,
        nullable=False
    )

    notes = Column(
        String
    )

    # -----------------------------
    # DERIVED FIELDS
    # -----------------------------

    gbp_net_amount = Column(
        Float,
        nullable=False
    )