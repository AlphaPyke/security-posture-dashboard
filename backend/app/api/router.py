from fastapi import APIRouter

from app.api.routes import auth, findings, github, repos, scans, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(github.router, prefix="/github", tags=["github"])
api_router.include_router(repos.router, prefix="/repos", tags=["repositories"])
api_router.include_router(scans.router, tags=["scans"])
api_router.include_router(findings.router, prefix="/findings", tags=["findings"])
