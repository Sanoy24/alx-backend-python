#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org data"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
