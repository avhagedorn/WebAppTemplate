from datetime import datetime

from polygon.rest.models.aggs import Agg
from pydantic import BaseModel

from project_name.utils.yfinance import format_date


class DataPoint(BaseModel):
    date: str
    left: float
    right: float
    left_percent_change: float
    right_percent_change: float

    @staticmethod
    def from_aggs(
        portfolio: Agg,
        spy: Agg,
        timeframe: str,
        start_portfolio: float = 0.0,
        start_spy: float = 0.0,
    ):
        scale_spy = start_portfolio / start_spy
        start_spy_scaled = start_spy * scale_spy

        return DataPoint(
            date=DataPoint._format_date(
                datetime.fromtimestamp(portfolio.timestamp / 1000),
                timeframe,
            ),
            left=portfolio.close,
            right=round(spy.close * scale_spy, 2),
            left_percent_change=round(
                ((portfolio.close - start_portfolio) / start_portfolio) * 100, 2
            ),
            right_percent_change=round(
                (((spy.close * scale_spy) - start_spy_scaled) / start_spy_scaled) * 100,
                2,
            ),
        )

    @staticmethod
    def from_yahoo(
        portfolio: float,
        spy: float,
        timestamp: int,
        timeframe: str,
        start_portfolio: float = 0.0,
        start_spy: float = 0.0,
        scale_spy_to_portfolio: bool = True,
    ):
        scale_spy = start_portfolio / start_spy if scale_spy_to_portfolio else 1
        start_spy_scaled = start_spy * scale_spy

        return DataPoint(
            date=format_date(
                timestamp,
                timeframe,
            ),
            left=round(portfolio, 2),
            right=round(spy * scale_spy, 2),
            left_percent_change=round(
                ((portfolio - start_portfolio) / start_portfolio) * 100, 2
            ),
            right_percent_change=round(
                (((spy * scale_spy) - start_spy_scaled) / start_spy_scaled) * 100, 2
            ),
        )


class ChartResponse(BaseModel):
    points: list[DataPoint]
    ticker: str
    timeframe: str
    last_price: float
    total_return: float
    total_return_percent: float
    total_return_spy: float
    total_return_percent_spy: float
    left_name: str
    right_name: str

    @staticmethod
    def from_data_points(data: list[DataPoint], ticker: str, timeframe: str):
        start_portfolio = data[0].left
        start_spy = data[0].right

        return ChartResponse(
            points=data,
            ticker=ticker,
            timeframe=timeframe,
            total_return=round((data[-1].left - start_portfolio), 2),
            total_return_percent=round(
                ((data[-1].left - start_portfolio) / start_portfolio) * 100, 2
            ),
            total_return_spy=round((data[-1].right - start_spy), 2),
            total_return_percent_spy=round(
                ((data[-1].right - start_spy) / start_spy) * 100, 2
            ),
            last_price=round(data[-1].left, 2),
            left_name="Portfolio",
            right_name="SPY",
        )

    @staticmethod
    def empty_response():
        return ChartResponse(
            points=[],
            ticker="",
            timeframe="",
            total_return=0,
            total_return_percent=0,
            total_return_spy=0,
            total_return_percent_spy=0,
            last_price=0,
            left_name="",
            right_name="",
        )


class CompareDataPoint(BaseModel):
    date: str
    left: float
    right: float
    left_percent_change: float
    right_percent_change: float

    @staticmethod
    def from_api(
        left: float,
        right: float,
        timestamp: int,
        timeframe: str,
        start_left: float = 0.0,
        start_right: float = 0.0,
    ):
        scaleRight = 100 / start_right
        scaleLeft = 100 / start_left

        return CompareDataPoint(
            date=format_date(
                timestamp,
                timeframe,
            ),
            left=round(left * scaleLeft, 2),
            right=round(right * scaleRight, 2),
            left_percent_change=round((right * scaleRight) - 100, 2),
            right_percent_change=round((left * scaleLeft) - 100, 2),
        )


class CompareChartResponse(BaseModel):
    points: list[CompareDataPoint]
    left_name: str
    right_name: str
    timeframe: str
    last_left: float
    last_right: float
    total_return_left: float
    total_return_percent_left: float
    total_return_right: float
    total_return_percent_right: float

    @staticmethod
    def from_data_points(
        data: list[CompareDataPoint],
        timeframe: str,
        left_name: str,
        right_name: str,
    ):
        start_left = data[0].left
        start_right = data[0].right

        return CompareChartResponse(
            points=data,
            left_name=left_name,
            right_name=right_name,
            timeframe=timeframe,
            total_return_left=round((data[-1].left - start_left), 2),
            total_return_percent_left=round(
                ((data[-1].left - start_left) / start_left) * 100, 2
            ),
            total_return_right=round((data[-1].right - start_right), 2),
            total_return_percent_right=round(
                ((data[-1].right - start_right) / start_right) * 100, 2
            ),
            last_left=round(data[-1].left, 2),
            last_right=round(data[-1].right, 2),
        )
