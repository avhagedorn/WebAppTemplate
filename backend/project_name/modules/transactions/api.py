import math
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import Portfolio
from project_name.db.models import Transaction
from project_name.db.models import User
from project_name.modules.transactions.models import CreateTransactionRequest
from project_name.modules.transactions.models import DisplayTransaction
from project_name.modules.transactions.models import GetTransactionsResponse
from project_name.utils.auth import get_current_user

router = APIRouter(prefix="/transactions")

"""
Handle transaction queries.
"""


@router.post("/create")
async def create_transaction(
    transaction: CreateTransactionRequest,
    current_user: User = Depends(get_current_user),
) -> DisplayTransaction:
    """
    Create a transaction.
    """
    with Session(get_sqlalchemy_engine()) as db_session:

        portfolio = (
            db_session.query(Portfolio)
            .filter(Portfolio.id == transaction.portfolio_id)
            .first()
        )

        if not portfolio or portfolio.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        transaction = Transaction(
            portfolio_id=transaction.portfolio_id,
            user_id=current_user.id,
            ticker=transaction.ticker,
            price_cents=int(transaction.price * 100),
            quantity=transaction.quantity,
            transaction_type=transaction.type,
            purchased_at=datetime.fromisoformat(transaction.purchased_at),
        )
        db_session.add(transaction)
        db_session.commit()
        return DisplayTransaction.from_db(transaction)


@router.post("/{transaction_id}/delete")
async def create_transaction(
    transaction_id: int, current_user: User = Depends(get_current_user)
) -> DisplayTransaction:
    """
    Delete a transaction.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        transaction = (
            db_session.query(Transaction)
            .filter(Transaction.user_id == current_user.id)
            .filter(Transaction.id == transaction_id)
            .first()
        )

        if not transaction or transaction.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )

        db_session.delete(transaction)
        db_session.commit()
        return DisplayTransaction.from_db(transaction)


@router.get("/stock/{ticker}")
async def get_stock_transactions(
    ticker: str, page: int = 0, page_size: int = 50, _: User = Depends(get_current_user)
) -> GetTransactionsResponse:
    """
    Get stock transactions.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        total_pages = math.ceil(
            db_session.query(Transaction).filter(Transaction.ticker == ticker).count()
            / page_size
        )

        transactions = (
            db_session.query(Transaction)
            .filter(Transaction.ticker == ticker.upper())
            .order_by(Transaction.purchased_at.desc())
            .offset(page * page_size)
            .limit(page_size)
            .all()
        )

        return GetTransactionsResponse(
            transactions=[DisplayTransaction.from_db(t) for t in transactions],
            page=page,
            total_pages=total_pages,
            page_size=page_size,
        )


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_transactions(
    portfolio_id: int,
    page_size: int = 50,
    page: int = 0,
    current_user: User = Depends(get_current_user),
):
    """
    Get all transactions within a portfolio.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolio = (
            db_session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        )

        if not portfolio or portfolio.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        total_pages = math.ceil(
            db_session.query(Transaction)
            .filter(Transaction.portfolio_id == portfolio_id)
            .count()
            / page_size
        )

        transactions = (
            db_session.query(Transaction)
            .filter(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.purchased_at.desc())
            .offset(page * page_size)
            .limit(page_size)
            .all()
        )

        return GetTransactionsResponse(
            transactions=[DisplayTransaction.from_db(t) for t in transactions],
            page=page,
            total_pages=total_pages,
            page_size=page_size,
        )


@router.get("/all")
async def get_all_transactions(
    page: int = 0, page_size: int = 50, current_user: User = Depends(get_current_user)
):
    """
    Get all transactions made by a user.
    """

    with Session(get_sqlalchemy_engine()) as db_session:

        total_pages = math.ceil(
            db_session.query(Transaction)
            .filter(Transaction.user_id == current_user.id)
            .count()
            / page_size
        )

        transactions = (
            db_session.query(Transaction)
            .filter(Transaction.user_id == current_user.id)
            .order_by(Transaction.purchased_at.desc())
            .offset(page * page_size)
            .limit(page_size)
            .all()
        )

        return GetTransactionsResponse(
            transactions=[DisplayTransaction.from_db(t) for t in transactions],
            page=page,
            total_pages=total_pages,
            page_size=page_size,
        )
