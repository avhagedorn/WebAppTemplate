from pydantic import BaseModel

from project_name.db.models import User


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class DisplayUser(BaseModel):
    username: str
    email: str
    created_at: str
    is_admin: bool

    @staticmethod
    def from_db(user: User):
        return DisplayUser(
            username=user.username,
            email=user.email,
            created_at=str(user.created_at),
            is_admin=user.is_admin,
        )


class ForgotPasswordRequest(BaseModel):
    email_or_username: str


class ResetPasswordUserRequest(BaseModel):
    password: str
    confirm_password: str
    reset_password_request_id: str
