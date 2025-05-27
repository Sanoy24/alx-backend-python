#!/usr/bin/env python3
"""A module for testing the client module."""
import unittest
from typing import Dict, List
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand(
        [
            ("google", {"login": "google"}),
            ("abc", {"login": "abc"}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mock_get_json: MagicMock) -> None:
        """Tests the `org` method."""
        mock_get_json.return_value = resp
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org, resp)
        url = f"https://api.github.com/orgs/{org}"
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns
        the correct URL from mocked org"""
        expected_url = "https://api.github.com/orgs/test-org/repos"

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}

            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = [
            {
                "id": 1,
                "name": "repo1",
                "license": {"key": "apache-2.0"},
            },
            {
                "id": 2,
                "name": "repo2",
                "license": {"key": "mit"},
            },
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:
            url = "https://api.github.com/orgs/test-org/repos"
            mock_repos_url.return_value = url

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
            ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
        ]
    )
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license` method."""
        gh_org_client = GithubOrgClient("google")
        self.assertEqual(gh_org_client.has_license(repo, key), expected)


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        },
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            return Mock(**{"json.return_value": route_payload[url]})

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method with mocked dependencies."""
        # Define payload
        test_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "gpl-3.0"}},
        ]

        mock_get_json.return_value = test_payload  # mock get_json return

        # Mock _public_repos_url property to return custom URL
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            url = "https://api.github.com/orgs/test-org/repos"
            mock_url.return_value = url

            client = GithubOrgClient("test-org")
            repos = client.public_repos()

            # Expected names from payload
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected)

            # Asserts
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
