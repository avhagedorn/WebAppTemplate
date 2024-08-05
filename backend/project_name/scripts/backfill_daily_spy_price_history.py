from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project_name.api_integrations.yfinance_client import yf_download
from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import IndexPriceHistory


def backfill_daily_spy_price_history():
    data = yf_download(
        tickers=["SPY"],
        period="max",
        interval="1d",
    )

    if data.empty:
        raise ValueError("No data found")

    try:
        with Session(get_sqlalchemy_engine()) as db_session:
            db_session.query(IndexPriceHistory).filter(
                IndexPriceHistory.ticker == "SPY"
            ).delete()

            price_history = []
            for date, price in zip(data.index, data["Open"]):
                price_history.append(
                    IndexPriceHistory(
                        date=date,
                        open_price_cents=int(price * 100),
                        ticker="SPY",
                    )
                )

                if len(price_history) == 1000:
                    db_session.bulk_save_objects(price_history)
                    price_history = []

            if price_history:
                db_session.bulk_save_objects(price_history)

            db_session.commit()
    except IntegrityError:
        pass  # Ignore duplicates
    except Exception as e:
        raise e


if __name__ == "__main__":
    backfill_daily_spy_price_history()
