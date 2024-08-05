from typing import Optional

from pydantic import BaseModel

from project_name.db.models import Portfolio
from project_name.modules.chart.models import ChartResponse


class CreatePortfolioRequest(BaseModel):
    name: str
    description: Optional[str] = None


class DisplayPortfolio(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    cash: float
    created_at: str

    @classmethod
    def from_db(cls, portfolio: Portfolio):
        return cls(
            id=portfolio.id,
            name=portfolio.name,
            cash=round(portfolio.cash_in_cents / 100, 2),
            description=portfolio.description,
            created_at=str(portfolio.created_at),
        )


class DisplayPortfolioWithChart(DisplayPortfolio):
    chart: ChartResponse

    @classmethod
    def from_db(cls, portfolio: Portfolio, chart: ChartResponse):
        return cls(
            id=portfolio.id,
            name=portfolio.name,
            cash=round(portfolio.cash_in_cents / 100, 2),
            description=portfolio.description,
            created_at=str(portfolio.created_at),
            chart=chart,
        )


class ListPortfoliosResponse(BaseModel):
    portfolios: list[DisplayPortfolio | DisplayPortfolioWithChart]
    strategy_display_option: int
