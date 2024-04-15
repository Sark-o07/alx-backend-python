#!/usr/bin/env python3
"""
a Test for the TestGithubOrgClient class
"""
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Dict
import unittest
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """
    testcases for the class methods
    """
    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": True})
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mocked_fn: MagicMock) -> None:
        """ Test for the org method
        """
        mocked_fn.return_value = MagicMock(return_value=resp)
        github_client = GithubOrgClient(org)
        self.assertEqual(github_client.org(), resp)
        mocked_fn.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """tests the `_public_repos_url` property.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }

            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }

        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient('google').public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {'key': "my_license"}}, "my_license", True),
        ({"license": {'key': "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected: bool) -> None:
        """Test for the `has_license` method."""
        test_response = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(test_response, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self, license="apache-2.0"):
        """Tests the `public_repos` method with an argument."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests.
        """
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
