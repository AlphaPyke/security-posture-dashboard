from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.repository import Repository
from app.models.scan import Scan, ScanCheck
from app.models.user import User
from app.schemas.finding import GitHubIssueCreateResponse
from app.services.github import GitHubIssueService
from app.services.tokens import TokenCipher

router = APIRouter()


@router.post("/{finding_id}/create-github-issue", response_model=GitHubIssueCreateResponse)
async def create_github_issue(
    finding_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GitHubIssueCreateResponse:
    finding = await db.get(ScanCheck, finding_id)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")

    scan = await db.get(Scan, finding.scan_id)
    repo = await db.get(Repository, scan.repository_id) if scan else None
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")

    token = TokenCipher().decrypt(current_user.encrypted_access_token)
    issue_url = await GitHubIssueService(token).create_issue(repo, finding)
    finding.github_issue_url = issue_url
    await db.commit()
    return GitHubIssueCreateResponse(issue_url=issue_url)
