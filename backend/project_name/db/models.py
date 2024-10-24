import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    reset_password_requests = relationship(
        "ResetPasswordRequest", back_populates="user", cascade="all, delete-orphan"
    )

class ResetPasswordRequest(Base):
    __tablename__ = "reset_password_request"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=func.now() + datetime.timedelta(hours=1)
    )

    user = relationship("User", back_populates="reset_password_requests")

    def is_expired(self) -> bool:
        return self.expires_at < datetime.datetime.now()
