from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)
    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    overall_score: Mapped[float | None] = mapped_column(Float)
    risk_level: Mapped[str | None] = mapped_column(String(32))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    raw_result_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    error_message: Mapped[str | None] = mapped_column(Text)

    repository = relationship("Repository", back_populates="scans")
    checks = relationship("ScanCheck", back_populates="scan", cascade="all, delete-orphan")


class ScanCheck(Base):
    __tablename__ = "scan_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id", ondelete="CASCADE"), index=True)
    check_name: Mapped[str] = mapped_column(String(255), index=True)
    score: Mapped[int] = mapped_column()
    reason: Mapped[str | None] = mapped_column(Text)
    details_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    remediation: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(32), index=True)
    github_issue_url: Mapped[str | None] = mapped_column(String(1024))

    scan = relationship("Scan", back_populates="checks")
