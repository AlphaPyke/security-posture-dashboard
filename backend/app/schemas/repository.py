from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GitHubRepositoryRead(BaseModel):
    github_owner: str
    github_repo: str
    full_name: str
    default_branch: str
    visibility: str
    is_private: bool


class RepositoryCreate(GitHubRepositoryRead):
    criticality: str = "medium"


class RepositoryRead(RepositoryCreate):
    id: int
    user_id: int
    selected_at: datetime

    model_config = ConfigDict(from_attributes=True)
