import json

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from sqlalchemy.orm import Session

from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import User
from project_name.utils.auth import get_current_user
from project_name.utils.email import send_data_request_email


router = APIRouter(prefix="/email")

"""
Handle email related operations.
"""


@router.get("/create-data-request")
async def data_request(
    background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)
):
    """
    Request user data.
    """

    def get_user_data(current_user: User):

        with Session(get_sqlalchemy_engine()) as session:
            user = session.query(User).filter(User.id == current_user.id).first()
            print(user.preferences.strategy_display_option)
            user_data = {
                "user_info": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": int(user.created_at.timestamp()),
                },
                "user_preferences": {
                    "strategy_display_option": user.preferences.strategy_display_option,
                },
                "portfolios": [
                    {
                        "id": portfolio.id,
                        "name": portfolio.name,
                        "description": portfolio.description,
                        "created_at": int(portfolio.created_at.timestamp()),
                    }
                    for portfolio in user.portfolios
                ],
                "transactions": [
                    {
                        "id": transaction.id,
                        "portfolio_id": transaction.portfolio_id,
                        "user_id": transaction.user_id,
                        "ticker": transaction.ticker,
                        "price_cents": transaction.price_cents,
                        "quantity": transaction.quantity,
                        "transaction_type": transaction.transaction_type,
                        "created_at": int(transaction.created_at.timestamp()),
                        "purchased_at": int(transaction.purchased_at.timestamp()),
                    }
                    for transaction in user.transactions
                ],
            }

            return json.dumps(user_data).encode("utf-8")

    background_tasks.add_task(
        send_data_request_email, current_user.email, get_user_data(current_user)
    )
    return {"message": "Data request email sent."}
