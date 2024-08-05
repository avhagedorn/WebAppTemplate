from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from project_name.configs import ACCESS_TOKEN_EXPIRE_MINUTES
from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import User
from project_name.db.models import UserPreferences
from project_name.modules.auth.models import DisplayUser
from project_name.modules.user.models import DisplayUserPreferences
from project_name.modules.user.models import UpdateUserPreferencesRequest
from project_name.modules.user.models import UpdateUserRequest
from project_name.utils.auth import create_access_token
from project_name.utils.auth import get_current_admin_user
from project_name.utils.auth import get_current_user
from project_name.utils.auth import get_password_hash

router = APIRouter(prefix="/user")

"""
Handle user management.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return DisplayUser.from_db(current_user)


@router.post("/update")
async def update_user(
    update_user_request: UpdateUserRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
):

    if update_user_request.old_password and not current_user.check_password(
        update_user_request.old_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    with Session(get_sqlalchemy_engine()) as db_session:
        current_user.email = update_user_request.email or current_user.email
        current_user.username = update_user_request.username or current_user.username

        if update_user_request.new_password:
            current_user.hashed_password = get_password_hash(
                update_user_request.new_password or update_user_request.old_password
            )

        db_session.add(current_user)
        db_session.commit()

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": current_user.username}, expires_delta=access_token_expires
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return DisplayUser.from_db(current_user)


@router.post("/delete")
async def delete_user(
    response: Response, current_user: User = Depends(get_current_user)
):
    with Session(get_sqlalchemy_engine()) as db_session:
        db_session.delete(current_user)
        db_session.commit()

    response.delete_cookie(key="access_token")
    return {"message": "User deleted"}


@router.get("/preferences")
async def read_user_preferences(
    current_user: User = Depends(get_current_user),
):
    with Session(get_sqlalchemy_engine()) as db_session:
        preferences = (
            db_session.query(UserPreferences).filter_by(user_id=current_user.id).first()
        )

        return DisplayUserPreferences.from_db(preferences)


@router.post("/preferences/update")
async def update_user_preferences(
    request: UpdateUserPreferencesRequest,
    current_user: User = Depends(get_current_user),
):
    with Session(get_sqlalchemy_engine()) as db_session:
        preferences = (
            db_session.query(UserPreferences).filter_by(user_id=current_user.id).first()
        )

        preferences.strategy_display_option = request.strategy_display_option
        db_session.commit()

        return DisplayUserPreferences.from_db(preferences)


"""
Admin endpoints
"""


@router.post("/promote/{username}")
async def promote_user(
    username: str,
    _: User = Depends(get_current_admin_user),
):

    with Session(get_sqlalchemy_engine()) as db_session:

        current_user = db_session.query(User).filter(User.username == username).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        current_user.is_admin = True
        current_user.save()

        return DisplayUser.from_db(current_user)


@router.post("/demote/{username}")
async def demote_user(
    username: str,
    _: User = Depends(get_current_admin_user),
):

    with Session(get_sqlalchemy_engine()) as db_session:
        current_user = db_session.query(User).filter(User.username == username).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        current_user.is_admin = False
        current_user.save()

        return DisplayUser.from_db(current_user)


@router.get("/list")
async def list_users(
    _: User = Depends(get_current_admin_user),
):
    with Session(get_sqlalchemy_engine()) as db_session:
        users = db_session.query(User).all()
        return [DisplayUser.from_db(user) for user in users]


@router.delete("/delete/{username}")
async def delete_user(
    username: str,
    _: User = Depends(get_current_admin_user),
):

    with Session(get_sqlalchemy_engine()) as db_session:
        current_user = db_session.query(User).filter(User.username == username).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete admin user",
            )

        db_session.delete(current_user)
        db_session.commit()

        return DisplayUser.from_db(current_user)
