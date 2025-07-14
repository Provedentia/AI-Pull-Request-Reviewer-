from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class GitHubUser(BaseModel):
    login: str
    id: int
    avatar_url: str
    html_url: str


class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    owner: GitHubUser
    html_url: str
    clone_url: str
    default_branch: str


class GitHubPullRequest(BaseModel):
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    user: GitHubUser
    html_url: str
    diff_url: str
    patch_url: str
    head: Dict[str, Any]
    base: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class GitHubWebhookPayload(BaseModel):
    action: str
    number: int
    pull_request: GitHubPullRequest
    repository: GitHubRepository
    sender: GitHubUser


class GitHubComment(BaseModel):
    body: str
    path: Optional[str] = None
    position: Optional[int] = None
    line: Optional[int] = None
    side: Optional[str] = "RIGHT"


class GitHubReviewRequest(BaseModel):
    body: str
    event: str = "COMMENT"
    comments: List[GitHubComment] = []