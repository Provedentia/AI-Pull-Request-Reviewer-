import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings
from app.schemas.github import GitHubComment, GitHubReviewRequest

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self):
        self.token = settings.github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PR-Reviewer-Bot"
        }

    async def get_pull_request_diff(self, owner: str, repo: str, pr_number: int) -> Optional[str]:
        """Fetch the diff for a pull request"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, 
                    headers={**self.headers, "Accept": "application/vnd.github.v3.diff"}
                )
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch PR diff: {e}")
            return None

    async def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> Optional[list]:
        """Fetch the files changed in a pull request"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch PR files: {e}")
            return None

    async def post_review_comment(
        self, 
        owner: str, 
        repo: str, 
        pr_number: int, 
        comment_body: str
    ) -> bool:
        """Post a review comment on a pull request"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        
        review_data = {
            "body": comment_body,
            "event": "COMMENT"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json=review_data, 
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Successfully posted review comment for PR #{pr_number}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Failed to post review comment: {e}")
            return False

    async def post_inline_comment(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        commit_sha: str,
        file_path: str,
        line_number: int,
        comment_body: str
    ) -> bool:
        """Post an inline comment on a specific line in a PR"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        
        comment_data = {
            "body": comment_body,
            "commit_id": commit_sha,
            "path": file_path,
            "line": line_number,
            "side": "RIGHT"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=comment_data,
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Successfully posted inline comment for PR #{pr_number}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Failed to post inline comment: {e}")
            return False

    async def get_pull_request_info(self, owner: str, repo: str, pr_number: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a pull request"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch PR info: {e}")
            return None