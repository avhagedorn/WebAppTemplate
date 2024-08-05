from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import Portfolio
from project_name.db.models import User
from project_name.db.models import UserPreferences
from project_name.modules.chart.api import get_portfolio_chart
from project_name.modules.portfolio.models import CreatePortfolioRequest
from project_name.modules.portfolio.models import DisplayPortfolio
from project_name.modules.portfolio.models import DisplayPortfolioWithChart
from project_name.modules.portfolio.models import ListPortfoliosResponse
from project_name.utils.auth import get_current_user

router = APIRouter(prefix="/portfolio")

"""
Handle user management.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/new")
async def create_portfolio(
    data: CreatePortfolioRequest, current_user: User = Depends(get_current_user)
):
    """
    Create a new portfolio.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolio = Portfolio(
            user_id=current_user.id,
            name=data.name,
            description=data.description,
        )
        db_session.add(portfolio)
        db_session.commit()
        return DisplayPortfolio.from_db(portfolio)


@router.get("/list")
async def list_portfolios(current_user: User = Depends(get_current_user)):
    """
    List all portfolios for the current user.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolios = (
            db_session.query(Portfolio)
            .filter_by(user_id=current_user.id)
            .order_by(Portfolio.created_at.desc())
            .all()
        )

        user_preferences = (
            db_session.query(UserPreferences).filter_by(user_id=current_user.id).first()
        )

        return ListPortfoliosResponse(
            portfolios=[
                DisplayPortfolioWithChart.from_db(
                    portfolio,
                    await get_portfolio_chart(portfolio.id, "ALL", current_user),
                )
                for portfolio in portfolios
            ],
            strategy_display_option=user_preferences.strategy_display_option,
        )


@router.get("/{portfolio_id}")
async def get_portfolio(
    portfolio_id: int, current_user: User = Depends(get_current_user)
):
    """
    Get a specific portfolio.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolio = (
            db_session.query(Portfolio)
            .filter_by(id=portfolio_id, user_id=current_user.id)
            .first()
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        return DisplayPortfolio.from_db(portfolio)


@router.post("/{portfolio_id}/update")
async def delete_portfolio(
    portfolio_id: int,
    data: CreatePortfolioRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Update a specific portfolio.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolio = (
            db_session.query(Portfolio)
            .filter_by(id=portfolio_id, user_id=current_user.id)
            .first()
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        portfolio.name = data.name
        portfolio.description = data.description
        db_session.commit()
        return DisplayPortfolio.from_db(portfolio)


@router.post("/{portfolio_id}/delete")
async def delete_portfolio(
    portfolio_id: int, current_user: User = Depends(get_current_user)
):
    """
    Delete a specific portfolio.
    """
    with Session(get_sqlalchemy_engine()) as db_session:
        portfolio = (
            db_session.query(Portfolio)
            .filter_by(id=portfolio_id, user_id=current_user.id)
            .first()
        )

        if not portfolio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found",
            )

        db_session.delete(portfolio)
        db_session.commit()
        return {"message": "Portfolio deleted successfully"}
