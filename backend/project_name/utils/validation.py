import re


def is_valid_email(email: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None


def is_valid_timeframe(timeframe: str) -> bool:
    return timeframe in ["1D", "1W", "1M", "3M", "YTD", "1Y", "ALL"]


def is_valid_compare_symbol(symbol: str) -> bool:
    stock_pattern = r"^STOCK:[a-zA-Z]+$"
    portfolio_pattern = r"^PORTFOLIO:\d+$"

    return (
        re.match(stock_pattern, symbol) is not None
        or re.match(portfolio_pattern, symbol) is not None
    )
