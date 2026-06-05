from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    id: int
    github_id: str
    username: str
    avatar_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
