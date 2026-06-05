from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.repository import Repository
from app.models.scan import Scan, ScanCheck
from app.models.user import User
from app.schemas.scan import ScanCheckRead, ScanRead
from app.services.queue import enqueue_scan

router = APIRouter()


@router.post(
    "/repos/{repo_id}/scans",
    response_model=ScanRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_scan(
    repo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Scan:
    repo = await db.get(Repository, repo_id)
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

    scan = Scan(repository_id=repo.id, status="queued")
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    enqueue_scan(scan.id)
    return scan


@router.get("/repos/{repo_id}/scans", response_model=list[ScanRead])
async def list_scans(
    repo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Scan]:
    repo = await db.get(Repository, repo_id)
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

    result = await db.execute(
        select(Scan).where(Scan.repository_id == repo_id).order_by(Scan.started_at.desc())
    )
    return list(result.scalars())


@router.get("/scans/{scan_id}", response_model=ScanRead)
async def get_scan(
    scan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Scan:
    scan = await db.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    repo = await db.get(Repository, scan.repository_id)
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    return scan


@router.get("/scans/{scan_id}/checks", response_model=list[ScanCheckRead])
async def get_scan_checks(
    scan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ScanCheck]:
    scan = await db.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    repo = await db.get(Repository, scan.repository_id)
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    result = await db.execute(
        select(ScanCheck).where(ScanCheck.scan_id == scan_id).order_by(ScanCheck.severity.desc())
    )
    return list(result.scalars())
