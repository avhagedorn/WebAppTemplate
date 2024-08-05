from fastapi import APIRouter
from fastapi import Depends

from project_name.api_integrations.yfinance_client import yf_ticker
from project_name.db.models import User
from project_name.modules.statistics.models import StockStatisticsResponse
from project_name.utils.auth import get_current_user

router = APIRouter(prefix="/statistics")

"""
Handle company and portfolio statistics related operations.
"""


@router.get("/stock/{ticker}")
async def get_stock_statistics(ticker: str, _: User = Depends(get_current_user)):
    """
    Get stock statistics.
    """

    ticker = yf_ticker(ticker)
    info = ticker.info

    return StockStatisticsResponse(
        website=info.get("website") or "",
        description=info.get("longBusinessSummary")
        or info.get("longDescription")
        or "",
        company_name=info.get("longName", ""),
        market_cap=info.get("marketCap", 0),
        eps=round(info.get("trailingEps", 0), 2),
        dividend_yield=round(info.get("dividendYield", 0) * 100, 2),
        pe_ratio=round(info.get("trailingPE", 0), 2),
        forward_pe=round(info.get("forwardPE", 0), 2),
        fifty_two_week_high=round(info.get("fiftyTwoWeekHigh", 0), 2),
        fifty_two_week_low=round(info.get("fiftyTwoWeekLow", 0), 2),
        beta=round(info.get("beta", 0), 2),
        debt_to_equity=round(info.get("debtToEquity", 0), 2),
        gross_margins=round(info.get("grossMargins", 0) * 100, 2),
        operating_margins=round(info.get("operatingMargins", 0) * 100, 2),
        profit_margins=round(info.get("profitMargins", 0) * 100, 2),
        ev_to_ebitda=round(info.get("enterpriseToEbitda", 0), 2),
        short_ratio=round(info.get("shortRatio", 0), 2),
        fcf_yield=round(
            info.get("freeCashflow", 0) / info.get("marketCap", 0) * 100, 2
        ),
        current_ratio=round(info.get("currentRatio", 0), 2),
        debt=info.get("totalDebt", 0),
        cash=info.get("totalCash", 0),
        return_on_equity=round(info.get("returnOnEquity", 0) * 100, 2),
        return_on_assets=round(info.get("returnOnAssets", 0) * 100, 2),
        peg_ratio=round(info.get("pegRatio", 0), 2),
        revenue_growth=round(info.get("revenueGrowth", 0) * 100, 2),
    )


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_statistics(
    portfolio_id: int, _: User = Depends(get_current_user)
):
    """
    Get portfolio statistics.
    """
