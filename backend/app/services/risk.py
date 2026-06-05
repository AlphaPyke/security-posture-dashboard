CRITICAL_CHECKS = {
    "Branch-Protection",
    "Token-Permissions",
    "Dangerous-Workflow",
    "Pinned-Dependencies",
}


def severity_for_score(check_name: str, score: int) -> str:
    if check_name in CRITICAL_CHECKS and score < 5:
        return "High"
    if score <= 2:
        return "High"
    if score <= 6:
        return "Medium"
    return "Low"


def calculate_risk_level(
    scorecard_score: float,
    *,
    is_private: bool,
    criticality: str,
    high_risk_check_count: int,
) -> str:
    public_repo_penalty = 10 if not is_private else 0
    criticality_penalty = {"low": 0, "medium": 10, "high": 25}.get(criticality, 10)
    high_risk_check_penalty = high_risk_check_count * 8
    risk_score = (
        ((10 - scorecard_score) * 10)
        + public_repo_penalty
        + criticality_penalty
        + high_risk_check_penalty
    )

    if risk_score >= 80:
        return "Critical"
    if risk_score >= 55:
        return "High"
    if risk_score >= 30:
        return "Medium"
    return "Low"
