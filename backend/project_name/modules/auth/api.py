import uuid
from datetime import timedelta

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project_name.configs import ACCESS_TOKEN_EXPIRE_MINUTES
from project_name.db.engine import get_sqlalchemy_engine
from project_name.db.models import ResetPasswordRequest
from project_name.db.models import User
from project_name.db.models import UserPreferences
from project_name.modules.auth.models import CreateUserRequest
from project_name.modules.auth.models import ForgotPasswordRequest
from project_name.modules.auth.models import LoginRequest
from project_name.modules.auth.models import ResetPasswordUserRequest
from project_name.modules.auth.models import Token
from project_name.utils.auth import authenticate_user
from project_name.utils.auth import create_access_token
from project_name.utils.auth import get_password_hash
from project_name.utils.email import send_reset_password_email
from project_name.utils.validation import is_valid_email

router = APIRouter(prefix="/auth")

"""
Handle token requests.
"""


@router.post("/token")
async def login_for_access_token(
    data: LoginRequest,
    response: Response,
) -> Token:
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register_user(
    data: CreateUserRequest,
    response: Response,
) -> Token:
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    elif len(data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters",
        )

    elif len(data.username) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 4 characters",
        )

    elif not is_valid_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email",
        )

    try:
        with Session(get_sqlalchemy_engine()) as db_session:
            user = User(
                username=data.username,
                email=data.email,
                hashed_password=get_password_hash(data.password),
                is_admin=True,
            )

            db_session.add(user)
            db_session.commit()

            user_preferences = UserPreferences(
                user_id=user.id, strategy_display_option=0
            )

            db_session.add(user_preferences)
            db_session.commit()

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
            return Token(access_token=access_token, token_type="bearer")

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
):
    user = None
    if is_valid_email(data.email_or_username):
        with Session(get_sqlalchemy_engine()) as db_session:
            user = (
                db_session.query(User).filter_by(email=data.email_or_username).first()
            )
            db_session.close()
    else:
        with Session(get_sqlalchemy_engine()) as db_session:
            user = (
                db_session.query(User)
                .filter_by(username=data.email_or_username)
                .first()
            )
            db_session.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    else:
        uuid_token = str(uuid.uuid4())
        with Session(get_sqlalchemy_engine()) as db_session:
            # Delete any existing reset password requests for the user
            db_session.query(ResetPasswordRequest).filter_by(user_id=user.id).delete()

            # Create a new reset password request
            reset_password_request = ResetPasswordRequest(
                user_id=user.id, uuid_token=uuid_token
            )
            db_session.add(reset_password_request)
            db_session.commit()

        background_tasks.add_task(
            send_reset_password_email,
            user.email,
            uuid_token,
        )

        return {"message": "Reset password email sent"}


@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordUserRequest,
    response: Response,
):
    with Session(get_sqlalchemy_engine()) as db_session:
        reset_password_request = (
            db_session.query(ResetPasswordRequest)
            .filter_by(uuid_token=data.reset_password_request_id)
            .first()
        )

        if not reset_password_request or reset_password_request.is_expired():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token",
            )

        if data.password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match",
            )

        user = (
            db_session.query(User).filter_by(id=reset_password_request.user_id).first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not find user associated with token",
            )

        user.hashed_password = get_password_hash(data.password)
        db_session.delete(reset_password_request)
        db_session.commit()

        response.delete_cookie(key="access_token")

        return {"message": "Password reset successfully"}
