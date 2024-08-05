from pydantic import BaseModel


class StockStatisticsResponse(BaseModel):
    company_name: str
    website: str
    description: str
    market_cap: float
    dividend_yield: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    beta: float
    eps: float
    pe_ratio: float
    forward_pe: float
    debt_to_equity: float
    ev_to_ebitda: float
    gross_margins: float
    operating_margins: float
    profit_margins: float
    short_ratio: float
    fcf_yield: float
    current_ratio: float
    debt: int
    cash: int
    return_on_equity: float
    return_on_assets: float
    peg_ratio: float
    revenue_growth: float
