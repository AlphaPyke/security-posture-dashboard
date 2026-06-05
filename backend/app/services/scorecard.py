import json
import subprocess
from dataclasses import dataclass
from typing import Any

from app.core.config import settings


@dataclass(frozen=True)
class ScorecardCheckResult:
    name: str
    score: int
    reason: str | None
    details: dict[str, Any] | None


@dataclass(frozen=True)
class ScorecardResult:
    score: float
    checks: list[ScorecardCheckResult]
    raw: dict[str, Any]


class ScorecardRunner:
    def run(self, full_name: str) -> ScorecardResult:
        if settings.scorecard_use_stub:
            return self._stub_result(full_name)

        completed = subprocess.run(
            [
                settings.scorecard_binary,
                f"--repo=https://github.com/{full_name}",
                "--format=json",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        payload = json.loads(completed.stdout)
        return self._parse(payload)

    def _parse(self, payload: dict[str, Any]) -> ScorecardResult:
        checks = [
            ScorecardCheckResult(
                name=check["name"],
                score=int(check.get("score", 0)),
                reason=check.get("reason"),
                details={"details": check.get("details", [])},
            )
            for check in payload.get("checks", [])
        ]
        return ScorecardResult(score=float(payload.get("score", 0)), checks=checks, raw=payload)

    def _stub_result(self, full_name: str) -> ScorecardResult:
        raw = {
            "repo": full_name,
            "score": 7.4,
            "checks": [
                {
                    "name": "Branch-Protection",
                    "score": 0,
                    "reason": "Default branch is not protected.",
                },
                {
                    "name": "Token-Permissions",
                    "score": 3,
                    "reason": "Workflow token permissions are too broad.",
                },
                {
                    "name": "Dependency-Update-Tool",
                    "score": 10,
                    "reason": "Dependency update tool is configured.",
                },
            ],
        }
        return self._parse(raw)
