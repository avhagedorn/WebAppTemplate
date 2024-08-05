from collections import defaultdict
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project_name.api_integrations.yfinance_client import yf_download
from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import Transaction
from project_name.db.models import User
from project_name.modules.common import get_all_portfolio_transactions
from project_name.modules.common import get_spy_prices_for_dates
from project_name.modules.positions.models import PortfolioPosition
from project_name.utils.auth import get_current_user

router = APIRouter(prefix="/positions")

"""
Handle position queries.
"""


@router.get("/all")
async def all_positions(
    current_user: User = Depends(get_current_user),
) -> List[PortfolioPosition]:
    """
    Aggregates all a user's positions by examining their transaction history.
    """
    db_session = Session(get_sqlalchemy_engine())

    # Query all transactions for the current user
    transactions = (
        db_session.query(Transaction)
        .where(Transaction.user_id == current_user.id)
        .all()
    )

    # Group transactions by ticker
    transactions_by_ticker = defaultdict(list)
    for transaction in transactions:
        transactions_by_ticker[transaction.ticker].append(transaction)

    # Convert the dictionary to a list of lists
    transactions_grouped_by_ticker = list(transactions_by_ticker.values())

    try:
        return _transactions_to_positions(transactions_grouped_by_ticker, db_session)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch positions"
        )


@router.get("/{portfolio_id}")
async def create_transaction(
    portfolio_id: int, current_user: User = Depends(get_current_user)
) -> List[PortfolioPosition]:
    """
    Aggregates all a portfolio's positions by examining the associated transaction history.
    """

    with Session(get_sqlalchemy_engine()) as db_session:

        transactions = get_all_portfolio_transactions(
            portfolio_id, current_user, db_session
        )

        if transactions:
            try:
                ticker_dict = defaultdict(list)
                for transaction in transactions:
                    ticker_dict[transaction.ticker].append(transaction)
                transactions_grouped_by_ticker = list(ticker_dict.values())
                return _transactions_to_positions(
                    transactions_grouped_by_ticker, db_session
                )
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to fetch positions",
                )
        else:
            return []


def _get_last_prices(tickers: List[str]):
    """
    Retrieves the last prices for the given tickers.
    """
    tickers_with_spy = list(set([*tickers, "SPY"]))
    prices = yf_download(
        tickers=tickers_with_spy,
        period="5d",  # Sometimes the API returns no data for 1d
        interval="1d",
    )

    return {
        ticker: int(prices[ticker]["Close"].iloc[-1] * 100)
        for ticker in tickers_with_spy
    }


def _transactions_to_positions(
    transactions_grouped_by_ticker: List[List[Transaction]],
    db_session: Optional[Session] = None,
) -> List[PortfolioPosition]:
    """
    Converts a list of transactions into a list of positions.
    """

    tickers = [
        transactions[0].ticker.upper()
        for transactions in transactions_grouped_by_ticker
    ]
    last_prices = _get_last_prices(tickers)

    db_session = db_session or Session(get_sqlalchemy_engine())

    def transactions_to_position(
        transactions: List[Transaction],
        db_session: Session,
    ) -> PortfolioPosition:
        transaction_dates = [t.purchased_at.date() for t in transactions]
        spy_date_to_price = get_spy_prices_for_dates(transaction_dates, db_session)

        shares = 0
        spy_shares = 0
        cost_basis_cents = 0

        realized_value_cents = 0
        realized_alpha_cents = 0

        for transaction in transactions:
            shares_delta = transaction.quantity
            spy_price_cents = spy_date_to_price.get(transaction.purchased_at.date())

            spy_shares_delta = (
                spy_shares * (shares_delta / shares)
                if spy_shares
                else (transaction.price_cents * shares_delta) / spy_price_cents
            )

            if transaction.transaction_type == "BUY":
                cost_basis_cents_delta = transaction.price_cents * shares_delta
                shares += shares_delta
                cost_basis_cents += cost_basis_cents_delta
                spy_shares += spy_shares_delta

            elif transaction.transaction_type == "SELL":
                cost_basis_cents_delta = (cost_basis_cents / shares) * shares_delta
                realized_value_cents += (
                    transaction.price_cents * shares_delta
                ) - cost_basis_cents_delta
                realized_alpha_cents += realized_value_cents - (
                    (spy_price_cents * spy_shares_delta) - cost_basis_cents_delta
                )
                shares -= shares_delta
                cost_basis_cents -= cost_basis_cents_delta
                spy_shares -= spy_shares_delta

        ticker = transactions[0].ticker
        ticker_current_price_cents = last_prices[ticker]
        spy_current_price_cents = last_prices["SPY"]

        ticker_current_equity_value_cents = int(shares * ticker_current_price_cents)
        ticker_return_percent = (
            ticker_current_equity_value_cents / cost_basis_cents
        ) * 100 - 100
        ticker_return_cents = ticker_current_equity_value_cents - cost_basis_cents

        spy_current_equity_value_cents = int(spy_shares * spy_current_price_cents)
        spy_return_percent = (
            spy_current_equity_value_cents / cost_basis_cents
        ) * 100 - 100
        spy_return_cents = spy_current_equity_value_cents - cost_basis_cents

        return PortfolioPosition(
            ticker=ticker,
            shares=shares,
            equity_value=round(ticker_current_equity_value_cents / 100, 2),
            return_percent=round(ticker_return_percent, 2),
            return_value=round(ticker_return_cents / 100, 2),
            alpha_percent=round((ticker_return_percent - spy_return_percent), 2),
            alpha_value=round((ticker_return_cents - spy_return_cents) / 100, 2),
            realized_value=round(realized_value_cents / 100, 2),
            realized_alpha=round(realized_alpha_cents / 100, 2),
        )

    return [
        transactions_to_position(transactions, db_session)
        for transactions in transactions_grouped_by_ticker
    ]
