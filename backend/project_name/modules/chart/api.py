from collections import defaultdict
from datetime import datetime
from typing import Dict
from typing import List
from typing import Tuple

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from project_name.api_integrations.polygon_client import rest_client
from project_name.api_integrations.yfinance_client import yf_download
from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import Portfolio
from project_name.db.models import Transaction
from project_name.db.models import User
from project_name.modules.chart.models import ChartResponse
from project_name.modules.chart.models import CompareChartResponse
from project_name.modules.chart.models import CompareDataPoint
from project_name.modules.chart.models import DataPoint
from project_name.modules.common import get_all_portfolio_transactions
from project_name.modules.common import get_all_transactions
from project_name.modules.common import get_spy_prices_for_dates
from project_name.utils.auth import get_current_user
from project_name.utils.polygon import timeframe_to_bar
from project_name.utils.time import split_by_date
from project_name.utils.validation import is_valid_compare_symbol
from project_name.utils.validation import is_valid_timeframe
from project_name.utils.yfinance import convert_timeframe_to_period
from project_name.utils.yfinance import get_start_from_timeframe
from project_name.utils.yfinance import interval_from_start_date


router = APIRouter(prefix="/chart")

"""
Handle chart related operations.
"""


@router.get("/stock/{ticker}/timeframe/{timeframe}")
async def get_stock_chart(
    ticker: str, timeframe: str, _: User = Depends(get_current_user)
):
    """
    Get stock chart.
    """

    if not is_valid_timeframe(timeframe):
        raise ValueError("Invalid timeframe")

    bar_args = timeframe_to_bar(timeframe)
    portfolio_response = []
    spy_response = []

    try:
        portfolio_response = rest_client.list_aggs(
            ticker=ticker.upper(),
            timeframe=bar_args.timeframe,
            multiplier=bar_args.multiplier,
            from_=bar_args.from_,
            to=bar_args.to,
        )

        spy_response = rest_client.list_aggs(
            ticker="SPY",
            timeframe=bar_args.timeframe,
            multiplier=bar_args.multiplier,
            from_=bar_args.from_,
            to=bar_args.to,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Request limit reached. Please try again later.",
        )

    portfolio_response = list(portfolio_response)
    spy_response = list(spy_response)
    start_portfolio = portfolio_response[0].close
    start_spy = spy_response[0].close

    return ChartResponse.from_data_points(
        data=[
            DataPoint.from_aggs(
                portfolio=portfolio,
                spy=spy,
                start_portfolio=start_portfolio,
                start_spy=start_spy,
                timeframe=timeframe,
            )
            for portfolio, spy in zip(portfolio_response, spy_response)
        ],
        ticker=ticker,
        timeframe=timeframe,
    )


@router.get("/v2/stock/{ticker}/timeframe/{timeframe}")
async def get_stock_chart_v2(
    ticker: str, timeframe: str, _: User = Depends(get_current_user)
):
    """
    Get stock chart v2.
    """

    if not is_valid_timeframe(timeframe):
        raise ValueError("Invalid timeframe")

    period, interval = convert_timeframe_to_period(timeframe)
    ticker = ticker.upper()
    data = []

    try:
        data = yf_download(
            tickers=[ticker, "SPY"],
            period=period,
            interval=interval,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Request limit reached. Please try again later.",
        )

    # If we only provide one ticker, yfinance will return a DataFrame with a single level column index.
    if ticker == "SPY":
        data = {"SPY": data}

    portfolio_response = data[ticker]["Close"]
    spy_response = data["SPY"]["Close"]

    if portfolio_response.empty or spy_response.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found.",
        )

    start_portfolio = portfolio_response.iloc[0]
    start_spy = spy_response.iloc[0]
    timestamps = portfolio_response.index

    return ChartResponse.from_data_points(
        data=[
            (
                DataPoint.from_yahoo(
                    portfolio=portfolio,
                    spy=spy,
                    start_portfolio=start_portfolio,
                    start_spy=start_spy,
                    timeframe=timeframe,
                    timestamp=timestamp.to_pydatetime(),
                )
            )
            for portfolio, spy, timestamp in zip(
                portfolio_response, spy_response, timestamps
            )
        ],
        ticker=ticker,
        timeframe=timeframe,
    )


@router.get("/compare")
async def compare(
    left_symbol: str,
    right_symbol: str,
    timeframe: str,
    _: User = Depends(get_current_user),
):

    if not is_valid_compare_symbol(left_symbol) or not is_valid_compare_symbol(
        right_symbol
    ):
        raise ValueError("Invalid symbol")

    if not is_valid_timeframe(timeframe):
        raise ValueError("Invalid timeframe")

    period, interval = convert_timeframe_to_period(timeframe)

    left_symbol_type, left_symbol = left_symbol.split(":")
    right_symbol_type, right_symbol = right_symbol.split(":")

    left_data = []
    right_data = []

    try:
        left_name = None
        right_name = None
        left_portfolio_id = None
        right_portfolio_id = None

        timestamps = []

        left_is_stock = left_symbol_type == "STOCK"
        right_is_stock = right_symbol_type == "STOCK"

        tickers = set()
        if left_is_stock:
            tickers.add(left_symbol)
            left_name = left_symbol
        else:
            left_portfolio_id = int(left_symbol)

        if right_is_stock:
            tickers.add(right_symbol)
            right_name = right_symbol
        else:
            right_portfolio_id = int(right_symbol)

        start_left, start_right = 0, 0

        if tickers:
            data = yf_download(
                tickers=list(tickers),
                period=period,
                interval=interval,
            )

            if left_is_stock and right_is_stock and left_symbol == right_symbol:
                left_data = data["Close"]
                right_data = data["Close"]
            else:
                if left_is_stock:
                    left_data = data[left_symbol]["Close"]
                    timestamps = data[left_symbol].index
                if right_is_stock:
                    right_data = data[right_symbol]["Close"]
                    timestamps = data[right_symbol].index

        if left_portfolio_id is not None or right_portfolio_id is not None:
            with Session(get_sqlalchemy_engine()) as db_session:
                if left_portfolio_id is not None:
                    left_portfolio = db_session.query(Portfolio).get(left_portfolio_id)
                    left_transactions = get_all_portfolio_transactions(
                        left_portfolio_id, left_portfolio.user
                    )
                    left_data, _, timestamps, _ = _get_chart_data_from_transactions(
                        left_transactions, timeframe
                    )
                    start_left = left_data[0]
                    left_name = left_portfolio.name
                if right_portfolio_id is not None:
                    right_portfolio = db_session.query(Portfolio).get(
                        right_portfolio_id
                    )
                    right_transactions = get_all_portfolio_transactions(
                        right_portfolio_id, right_portfolio.user
                    )
                    right_data, _, timestamps, _ = _get_chart_data_from_transactions(
                        right_transactions, timeframe
                    )
                    start_right = right_data[0]
                    right_name = right_portfolio.name

        if left_is_stock:
            start_left = left_data.iloc[0]
        if right_is_stock:
            start_right = right_data.iloc[0]

        return CompareChartResponse.from_data_points(
            data=[
                CompareDataPoint.from_api(
                    left=left,
                    right=right,
                    timestamp=timestamp,
                    timeframe=timeframe,
                    start_left=start_left,
                    start_right=start_right,
                )
                for left, right, timestamp in zip(left_data, right_data, timestamps)
            ],
            timeframe=timeframe,
            left_name=left_name,
            right_name=right_name,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Request limit reached. Please try again later.",
        )


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_chart(
    portfolio_id: int, timeframe: str, current_user: User = Depends(get_current_user)
):
    """
    Get portfolio chart.
    """
    transactions = get_all_portfolio_transactions(portfolio_id, current_user)

    if not transactions:
        return ChartResponse.empty_response()

    portfolio_value, spy_value, timestamps, cost_basis_cents = (
        _get_chart_data_from_transactions(transactions, timeframe)
    )

    return ChartResponse.from_data_points(
        data=[
            DataPoint.from_yahoo(
                portfolio=portfolio,
                spy=spy,
                start_portfolio=cost_basis_cents,
                start_spy=cost_basis_cents,
                timeframe=timeframe,
                timestamp=timestamp,
                scale_spy_to_portfolio=False,
            )
            for portfolio, spy, timestamp in zip(portfolio_value, spy_value, timestamps)
        ],
        ticker="Portfolio",
        timeframe=timeframe,
    )


@router.get("/summary")
async def get_summary_chart(
    timeframe: str, current_user: User = Depends(get_current_user)
):
    """
    Get summary chart.
    """
    transactions = get_all_transactions(current_user)

    if not transactions:
        return ChartResponse.empty_response()

    portfolio_value, spy_value, timestamps, cost_basis_cents = (
        _get_chart_data_from_transactions(transactions, timeframe)
    )

    return ChartResponse.from_data_points(
        data=[
            DataPoint.from_yahoo(
                portfolio=portfolio,
                spy=spy,
                start_portfolio=cost_basis_cents,
                start_spy=cost_basis_cents,
                timeframe=timeframe,
                timestamp=timestamp,
                scale_spy_to_portfolio=False,
            )
            for portfolio, spy, timestamp in zip(portfolio_value, spy_value, timestamps)
        ],
        ticker="Portfolio",
        timeframe=timeframe,
    )


def _get_chart_data_from_transactions(
    transactions: List[Transaction], timeframe: str
) -> Tuple[List[int], List[int], List[datetime], int]:
    """
    Get the chart data from the given transactions.
    """

    # Step 1: Get all tickers from the transactions
    tickers = list(set(["SPY"] + [transaction.ticker for transaction in transactions]))

    # Step 2: Get all SPY prices for the transaction dates
    transaction_dates = [
        transaction.purchased_at.date() for transaction in transactions
    ]
    spy_date_to_price = get_spy_prices_for_dates(transaction_dates)

    # Step 3: Get pre- and in-timeframe transactions
    timeframe_start = get_start_from_timeframe(timeframe)
    pre_timeframe_transactions, timeframe_transactions = split_by_date(
        transactions, timeframe_start.date()
    )

    # Step 3: Get all holdings from before the start of the timeframe
    initial_holdings, cash_holding_cents, initial_spy_shares, cost_basis_cents = (
        _get_initial_holdings(pre_timeframe_transactions, spy_date_to_price)
    )

    # Step 4: Get all the data points for the timeframe
    ticker_data, timestamps = _get_ticker_data(
        tickers, timeframe, transactions[0].purchased_at
    )

    # Step 5: Calculate the portfolio value for each data point in the timeframe
    portfolio_value, spy_value, cost_basis_cents = _calculate_portfolio_values(
        ticker_data,
        initial_holdings,
        cash_holding_cents,
        initial_spy_shares,
        cost_basis_cents,
        timeframe_transactions,
        spy_date_to_price,
    )

    # Round to the nearest cent
    portfolio_value = [round(value, 2) for value in portfolio_value]
    spy_value = [round(value, 2) for value in spy_value]

    return portfolio_value, spy_value, timestamps, cost_basis_cents


def _get_initial_holdings(
    transactions: List[Transaction], spy_date_to_price: Dict[datetime, int]
) -> Tuple[Dict[str, int], int, int, int]:
    """
    Calculates the initial holdings, cash holdings, initial SPY shares, and cost basis cents
    before the start of the timeframe.
    """
    initial_holdings = defaultdict(int)
    cash_holding_cents = 0
    initial_spy_shares = 0
    cost_basis_cents = 0

    for transaction in transactions:
        initial_holdings, cash_holding_cents, initial_spy_shares, cost_basis_cents = (
            _update_holdings(
                transaction,
                spy_date_to_price,
                initial_holdings,
                cash_holding_cents,
                initial_spy_shares,
                cost_basis_cents,
            )
        )

    return initial_holdings, cash_holding_cents, initial_spy_shares, cost_basis_cents


def _get_ticker_data(
    tickers: List[str], timeframe: str, first_transaction_date: datetime
) -> Tuple[List[Dict[str, int]], List[datetime]]:
    """
    Retrieves the ticker data for the given tickers and timeframe.
    """
    period, _ = convert_timeframe_to_period(timeframe)
    interval_start_timestamp = get_start_from_timeframe(timeframe)

    if period == "max":
        interval_start_timestamp = first_transaction_date

    interval = interval_from_start_date(interval_start_timestamp)
    data = yf_download(
        tickers=tickers, interval=interval, start=interval_start_timestamp
    )

    timestamps = data[tickers[0]].index
    ticker_to_prices = {ticker: data[ticker]["Close"] for ticker in tickers}
    ticker_data = [
        {
            **dict(zip(ticker_to_prices.keys(), values)),
            "timestamp": timestamp.date(),
        }
        for values, timestamp in zip(zip(*ticker_to_prices.values()), timestamps)
    ]

    return ticker_data, timestamps


def _update_holdings(
    transaction: Transaction,
    spy_date_to_price: Dict[datetime, int],
    initial_holdings: Dict[str, int],
    cash_holding_cents: int,
    initial_spy_shares: float,
    cost_basis_cents: int,
) -> Tuple[Dict[str, int], int, float, int]:
    """
    Updates the holdings, cash holdings, initial SPY shares, and cost basis based on a transaction.
    """
    current_spy_price = spy_date_to_price.get(transaction.purchased_at.date())
    transaction_cost = transaction.quantity * transaction.price_cents

    if transaction.transaction_type == "BUY":
        initial_holdings[transaction.ticker] += transaction.quantity
        initial_spy_shares += transaction_cost // current_spy_price
        cost_basis_cents += max(0, transaction_cost - cash_holding_cents)
        cash_holding_cents = max(0, cash_holding_cents - transaction_cost)
    else:
        initial_holdings[transaction.ticker] -= transaction.quantity
        cash_holding_cents += transaction_cost

    return initial_holdings, cash_holding_cents, initial_spy_shares, cost_basis_cents


def _calculate_portfolio_values(
    ticker_data: List[Dict[str, int]],
    initial_holdings: Dict[str, int],
    cash_holding_cents: int,
    initial_spy_shares: float,
    cost_basis_cents: int,
    transactions: List[Transaction],
    spy_date_to_price: Dict[datetime, int],
) -> Tuple[List[int], List[int], List[int]]:
    """
    Calculates the portfolio values, cost basis values, and SPY values for each data point in
    the timeframe.
    """

    portfolio_value = []
    cost_basis_value = []
    spy_value = []
    timeframe_transactions_index = 0

    for data_point in ticker_data:
        if timeframe_transactions_index < len(transactions):
            transaction = transactions[timeframe_transactions_index]
            if data_point["timestamp"] >= transaction.purchased_at.date():
                (
                    initial_holdings,
                    cash_holding_cents,
                    initial_spy_shares,
                    cost_basis_cents,
                ) = _update_holdings(
                    transaction,
                    spy_date_to_price,
                    initial_holdings,
                    cash_holding_cents,
                    initial_spy_shares,
                    cost_basis_cents,
                )
                timeframe_transactions_index += 1

        portfolio_value.append(
            sum(
                [
                    initial_holdings[ticker] * data_point[ticker]
                    for ticker in initial_holdings.keys()
                ]
            )
            + cash_holding_cents / 100
        )
        spy_value.append(initial_spy_shares * data_point["SPY"])
        cost_basis_value.append(cost_basis_cents / 100)

    for idx, value in enumerate(cost_basis_value):
        if value < cost_basis_cents / 100:
            cost_basis_diff = cost_basis_cents / 100 - cost_basis_value[idx]
            portfolio_value[idx] += cost_basis_diff
            spy_value[idx] += cost_basis_diff

    return portfolio_value, spy_value, cost_basis_cents
