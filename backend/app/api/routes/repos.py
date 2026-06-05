from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.repository import Repository
from app.models.user import User
from app.schemas.repository import RepositoryCreate, RepositoryRead

router = APIRouter()


@router.post("", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
async def select_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Repository:
    repo = Repository(user_id=current_user.id, **payload.model_dump())
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    return repo


@router.get("", response_model=list[RepositoryRead])
async def list_selected_repositories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Repository]:
    result = await db.execute(select(Repository).where(Repository.user_id == current_user.id))
    return list(result.scalars())


@router.get("/{repo_id}", response_model=RepositoryRead)
async def get_repository(
    repo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Repository:
    repo = await db.get(Repository, repo_id)
    if repo is None or repo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    return repo
