from pydantic import BaseModel


class SearchResult(BaseModel):
    name: str
    ticker: str


class PortfolioResult(BaseModel):
    name: str
    id: int


class SearchResponse(BaseModel):
    ticker_results: list[SearchResult]
    portfolio_results: list[PortfolioResult]
