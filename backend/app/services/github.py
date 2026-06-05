from dataclasses import dataclass
from urllib.parse import urlencode

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.repository import Repository
from app.models.scan import ScanCheck
from app.models.user import User


@dataclass(frozen=True)
class GitHubToken:
    access_token: str
    token_type: str
    scope: str


@dataclass(frozen=True)
class GitHubProfile:
    github_id: str
    username: str
    avatar_url: str | None


class GitHubOAuthService:
    def authorization_url(self) -> str:
        params = urlencode(
            {
                "client_id": settings.github_client_id,
                "redirect_uri": f"{settings.api_base_url}/auth/github/callback",
                "scope": settings.github_oauth_scopes,
            }
        )
        return f"https://github.com/login/oauth/authorize?{params}"

    async def exchange_code(self, code: str) -> GitHubToken:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code,
                    "redirect_uri": f"{settings.api_base_url}/auth/github/callback",
                },
            )
            response.raise_for_status()
            payload = response.json()

        return GitHubToken(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "bearer"),
            scope=payload.get("scope", ""),
        )

    async def fetch_user(self, access_token: str) -> GitHubProfile:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                },
            )
            response.raise_for_status()
            payload = response.json()

        return GitHubProfile(
            github_id=str(payload["id"]),
            username=payload["login"],
            avatar_url=payload.get("avatar_url"),
        )

    async def upsert_user(
        self,
        db: AsyncSession,
        profile: GitHubProfile,
        encrypted_access_token: str,
    ) -> User:
        result = await db.execute(select(User).where(User.github_id == profile.github_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                github_id=profile.github_id,
                username=profile.username,
                avatar_url=profile.avatar_url,
                encrypted_access_token=encrypted_access_token,
            )
            db.add(user)
        else:
            user.username = profile.username
            user.avatar_url = profile.avatar_url
            user.encrypted_access_token = encrypted_access_token

        await db.commit()
        await db.refresh(user)
        return user


class GitHubRepositoryService:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def list_repositories(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                "https://api.github.com/user/repos",
                params={
                    "per_page": 100,
                    "sort": "updated",
                    "affiliation": "owner,collaborator,organization_member",
                },
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Accept": "application/vnd.github+json",
                },
            )
            response.raise_for_status()
            repos = response.json()

        return [
            {
                "github_owner": repo["owner"]["login"],
                "github_repo": repo["name"],
                "full_name": repo["full_name"],
                "default_branch": repo.get("default_branch") or "main",
                "visibility": repo.get("visibility")
                or ("private" if repo.get("private") else "public"),
                "is_private": bool(repo.get("private")),
            }
            for repo in repos
        ]


class GitHubIssueService:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def create_issue(self, repo: Repository, finding: ScanCheck) -> str:
        title = f"[Security Posture] Fix {finding.check_name}"
        body = "\n".join(
            [
                (
                    "OpenSSF Scorecard detected a failed check: "
                    f"**{finding.check_name}**."
                ),
                "",
                f"Reason: {finding.reason or 'No reason provided.'}",
                "",
                "Recommended actions:",
                finding.remediation or "Review the Scorecard documentation for this check.",
                "",
                f"Risk: {finding.severity}",
            ]
        )
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"https://api.github.com/repos/{repo.full_name}/issues",
                json={"title": title, "body": body},
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Accept": "application/vnd.github+json",
                },
            )
            response.raise_for_status()
            payload = response.json()

        return payload["html_url"]
