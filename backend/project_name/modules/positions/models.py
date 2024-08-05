from pydantic import BaseModel


class PortfolioPosition(BaseModel):
    ticker: str
    shares: int
    equity_value: float
    return_percent: float
    return_value: float
    alpha_percent: float
    alpha_value: float
    realized_value: float
    realized_alpha: float
