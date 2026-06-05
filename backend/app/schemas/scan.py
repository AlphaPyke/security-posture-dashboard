from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ScanRead(BaseModel):
    id: int
    repository_id: int
    status: str
    overall_score: float | None
    risk_level: str | None
    started_at: datetime
    completed_at: datetime | None
    error_message: str | None

    model_config = ConfigDict(from_attributes=True)


class ScanCheckRead(BaseModel):
    id: int
    scan_id: int
    check_name: str
    score: int
    reason: str | None
    details_json: dict[str, Any] | None
    remediation: str | None
    severity: str
    github_issue_url: str | None

    model_config = ConfigDict(from_attributes=True)
