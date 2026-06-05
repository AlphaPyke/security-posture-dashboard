REMEDIATIONS = {
    "Branch-Protection": (
        "Enable branch protection, require pull request reviews, require status checks, "
        "and block force pushes."
    ),
    "Token-Permissions": (
        "Set GitHub Actions token permissions to read-only by default and grant write "
        "access only per workflow."
    ),
    "Dependency-Update-Tool": (
        "Enable Dependabot or another dependency update tool for supported package ecosystems."
    ),
    "Code-Review": (
        "Require at least one approving pull request review before merging to the default branch."
    ),
    "Pinned-Dependencies": (
        "Pin GitHub Actions and dependencies to immutable versions where possible."
    ),
}


def remediation_for_check(check_name: str) -> str:
    return REMEDIATIONS.get(
        check_name,
        "Review the OpenSSF Scorecard check guidance and document the chosen fix.",
    )
