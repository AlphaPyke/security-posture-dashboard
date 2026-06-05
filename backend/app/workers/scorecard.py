import asyncio
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.repository import Repository
from app.models.scan import Scan, ScanCheck
from app.services.remediation import remediation_for_check
from app.services.risk import calculate_risk_level, severity_for_score
from app.services.scorecard import ScorecardRunner


def run_scan_job(scan_id: int) -> None:
    asyncio.run(_run_scan_job(scan_id))


async def _run_scan_job(scan_id: int) -> None:
    async with async_session() as db:
        scan = await db.get(Scan, scan_id)
        if scan is None:
            return

        repo = await db.get(Repository, scan.repository_id)
        if repo is None:
            scan.status = "failed"
            scan.error_message = "Repository not found"
            await db.commit()
            return

        scan.status = "running"
        await db.commit()
        try:
            result = ScorecardRunner().run(repo.full_name)
            await _persist_result(db, scan, repo, result)
        except Exception as exc:
            scan.status = "failed"
            scan.error_message = str(exc)
            scan.completed_at = datetime.now(UTC)
            await db.commit()


async def _persist_result(db: AsyncSession, scan: Scan, repo: Repository, result) -> None:
    high_risk_count = 0
    scan.checks.clear()

    for check in result.checks:
        severity = severity_for_score(check.name, check.score)
        if severity in {"High", "Critical"}:
            high_risk_count += 1
        scan.checks.append(
            ScanCheck(
                check_name=check.name,
                score=check.score,
                reason=check.reason,
                details_json=check.details,
                remediation=remediation_for_check(check.name),
                severity=severity,
            )
        )

    scan.status = "completed"
    scan.overall_score = result.score
    scan.risk_level = calculate_risk_level(
        result.score,
        is_private=repo.is_private,
        criticality=repo.criticality,
        high_risk_check_count=high_risk_count,
    )
    scan.raw_result_json = result.raw
    scan.completed_at = datetime.now(UTC)
    await db.commit()
