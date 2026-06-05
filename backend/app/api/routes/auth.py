from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.services.github import GitHubOAuthService
from app.services.tokens import TokenCipher

router = APIRouter()


@router.get("/github/login")
async def github_login() -> RedirectResponse:
    oauth = GitHubOAuthService()
    return RedirectResponse(oauth.authorization_url())


@router.get("/github/callback")
async def github_callback(
    code: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    if not settings.github_client_id or not settings.github_client_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub OAuth is not configured",
        )

    oauth = GitHubOAuthService()
    token = await oauth.exchange_code(code)
    profile = await oauth.fetch_user(token.access_token)
    encrypted_token = TokenCipher().encrypt(token.access_token)
    user = await oauth.upsert_user(db, profile, encrypted_token)
    request.session["user_id"] = user.id
    return RedirectResponse(f"{settings.frontend_base_url}/dashboard")


@router.post("/logout")
async def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"status": "logged_out"}
