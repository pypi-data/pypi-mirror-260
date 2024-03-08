# pylint: disable=too-many-arguments
"""Adapter for GitHub API."""
from typing import Dict, Optional, List
import requests


class GithubAdapter:
    """Functions to interact with the GitHub API."""

    def __init__(
        self, api_url: str, github_token: str, exception_cls: Optional[Exception] = None
    ) -> None:
        """Initialize the adapter."""
        self.api_url = api_url
        self.github_token = github_token
        self.exception_cls = exception_cls or Exception

    def make_api(self, api_path: str, json_payload: str, is_post: bool) -> Dict:
        """Make API calls to github"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.github_token}",
            "User-Agent": "opendapi.org",
        }
        if is_post:
            response = requests.post(
                f"{self.api_url}/{api_path}",
                headers=headers,
                json=json_payload,
                timeout=30,
            )
        else:
            response = requests.get(
                f"{self.api_url}/{api_path}",
                params=json_payload,
                headers=headers,
                timeout=30,
            )
        # Error on any status code other than 201 (created) or 422 (PR already exists)
        if response.status_code > 400 and response.status_code != 422:
            raise self.exception_cls(
                "Something went wrong! "
                f"API failure with {response.status_code} for {api_path}. "
                f"Response: {response.text}"
            )

        return response.json()

    def add_pull_request_comment(self, pull_request_number: int, message: str):
        """Add a comment to the pull request."""
        self.make_api(
            f"issues/{pull_request_number}/comments",
            {"body": message},
            is_post=True,
        )

    def get_pull_requests(
        self, repo_owner: str, base: str, head: str, state: str
    ) -> List[Dict]:
        """Get pull requests from Github."""
        return self.make_api(
            "pulls",
            {
                "head": f"{repo_owner}:{head}",
                "base": base,
                "state": state,
            },
            is_post=False,
        )

    def get_merged_pull_requests(
        self, repo_owner: str, base: str, head: str
    ) -> List[Dict]:
        """Get merged pull requests from Github."""
        pull_requests = self.make_api(
            "pulls",
            {
                "head": f"{repo_owner}:{head}",
                "base": base,
                "state": "closed",
                "sort": "updated",
            },
            is_post=False,
        )
        return sorted(
            [pr for pr in pull_requests if pr.get("merged_at")],
            key=lambda pr: pr.get("merged_at"),
            reverse=True,
        )

    def create_pull_request_if_not_exists(
        self, repo_owner: str, title: str, body: str, base: str, head: str
    ) -> int:
        """Create or update a pull request on Github."""
        # Check if a pull request already exists for this branch using list pull requests
        pull_requests = self.get_pull_requests(repo_owner, base, head, "open")

        if not pull_requests:
            # Create a new pull request if one doesn't exist
            response_json = self.make_api(
                "pulls",
                {"title": title, "body": body, "head": head, "base": base},
                is_post=True,
            )
            pull_request_number = response_json.get("number")
        else:
            pull_request_number = pull_requests[0].get("number")

        return pull_request_number
