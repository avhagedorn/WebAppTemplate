from typing import Optional

from pydantic import BaseModel

from project_name.db.models import UserPreferences


class UpdateUserPreferencesRequest(BaseModel):
    strategy_display_option: int


class DisplayUserPreferences(BaseModel):
    strategy_display_option: int

    @staticmethod
    def from_db(preferences: UserPreferences):
        return DisplayUserPreferences(
            strategy_display_option=preferences.strategy_display_option
        )


class UpdateUserRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
