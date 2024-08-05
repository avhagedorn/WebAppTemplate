from enum import Enum
from typing import List

from pydantic import BaseModel

from project_name.db.models import Transaction


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class CreateTransactionRequest(BaseModel):
    quantity: float
    price: float
    ticker: str
    portfolio_id: int
    purchased_at: str
    type: TransactionType


class DisplayTransaction(BaseModel):
    id: int
    shares: float
    price: float
    ticker: str
    portfolio_id: int
    type: TransactionType
    date: str

    @staticmethod
    def from_db(transaction: Transaction):
        return DisplayTransaction(
            id=transaction.id,
            shares=transaction.quantity,
            price=round(transaction.price_cents / 100, 2),
            ticker=transaction.ticker,
            portfolio_id=transaction.portfolio_id,
            type=transaction.transaction_type,
            date=transaction.purchased_at.strftime("%Y-%m-%d"),
        )


class GetTransactionsResponse(BaseModel):
    transactions: List[DisplayTransaction]
    page: int
    total_pages: int
    page_size: int
