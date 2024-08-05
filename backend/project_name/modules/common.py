from datetime import date
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import IndexPriceHistory
from project_name.db.models import Portfolio
from project_name.db.models import Transaction
from project_name.db.models import User


def get_all_portfolio_transactions(
    portfolio_id: int, current_user: User, db_session: Optional[Session] = None
) -> List[Transaction]:

    db_session = db_session or Session(get_sqlalchemy_engine())
    portfolio = db_session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    if not portfolio or portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return (
        db_session.query(Transaction)
        .filter(Transaction.portfolio_id == portfolio.id)
        .order_by(Transaction.purchased_at.asc(), Transaction.created_at.asc())
        .all()
    )


def get_all_transactions(current_user: User) -> List[Transaction]:
    with Session(get_sqlalchemy_engine()) as db_session:
        return (
            db_session.query(Transaction)
            .join(Portfolio)
            .filter(Portfolio.user_id == current_user.id)
            .order_by(Transaction.purchased_at.asc(), Transaction.created_at.asc())
            .all()
        )


def get_spy_prices_for_dates(
    dates: List[date], db_session: Optional[Session] = None
) -> Dict[datetime, int]:
    """
    Retrieves the SPY prices for the dates of the given transactions.
    """

    db_session = db_session or Session(get_sqlalchemy_engine())

    spy_prices = (
        db_session.query(IndexPriceHistory)
        .filter(IndexPriceHistory.ticker == "SPY")
        .filter(IndexPriceHistory.date.in_(dates))
        .all()
    )
    return {price.date.date(): price.open_price_cents for price in spy_prices}
