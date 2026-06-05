from pydantic import BaseModel


class GitHubIssueCreateResponse(BaseModel):
    issue_url: str
