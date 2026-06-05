from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.repository import GitHubRepositoryRead
from app.services.github import GitHubRepositoryService
from app.services.tokens import TokenCipher

router = APIRouter()


@router.get("/repos", response_model=list[GitHubRepositoryRead])
async def list_github_repositories(current_user: User = Depends(get_current_user)) -> list[dict]:
    access_token = TokenCipher().decrypt(current_user.encrypted_access_token)
    return await GitHubRepositoryService(access_token).list_repositories()
