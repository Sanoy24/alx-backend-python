#!/usr/bin/env python3
"""A GitHub org client"""
from typing import Dict, List
from utils import get_json, access_nested_map, memoize


class GithubOrgClient:
    """A GitHub org client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name"""
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch organization data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Extract repos_url from org data"""
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Get repositories payload"""
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Get public repositories with optional license filter"""
        repos = self.repos_payload
        return [
            repo["name"]
            for repo in repos
            if license is None or self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if a repo has the specified license"""
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
