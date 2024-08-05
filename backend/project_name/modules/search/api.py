import requests
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import Portfolio
from project_name.db.models import User
from project_name.modules.search.models import PortfolioResult
from project_name.modules.search.models import SearchResponse
from project_name.modules.search.models import SearchResult
from project_name.utils.auth import get_current_user

router = APIRouter(prefix="/search")

"""
Handle search related operations.
"""


@router.get("/stock")
async def search(q: str = "", current_user: User = Depends(get_current_user)):
    """
    Search for a stock.
    """

    if not q:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing query parameter",
        )

    # TODO: Add this to the yfinance library
    # Pull request: https://github.com/ranaroussi/yfinance/pull/1949
    response = requests.get(
        "https://query1.finance.yahoo.com/v1/finance/search",
        params={"q": q, "newsCount": 0, "quotesCount": 5, "enableFuzzyQuery": False},
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        },
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch data",
        )

    with Session(get_sqlalchemy_engine()) as db_session:
        portfolios = (
            db_session.query(Portfolio)
            .filter(Portfolio.user_id == current_user.id)
            .filter(Portfolio.name.ilike(f"%{q}%"))
        )

    ticker_results = [
        (
            SearchResult(
                ticker=quote["symbol"],
                name=quote["shortname"],
            )
            if quote.get("quoteType") == "EQUITY"
            else None
        )
        for quote in response.json().get("quotes", [])
    ]

    portfolio_results = [
        PortfolioResult(
            id=portfolio.id,
            name=portfolio.name,
        )
        for portfolio in portfolios
    ]

    return SearchResponse(
        ticker_results=[ticker for ticker in ticker_results if ticker],
        portfolio_results=portfolio_results,
    )
