from typing import Optional

from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
