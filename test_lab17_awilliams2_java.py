import unittest
from unittest.mock import patch
from Lab17_awilliams2_java import GitHubAPIClient, RepoDataParser, RepoPlotter

MOCK_RESPONSE = {
    "items": [
        {
            "name": "spring-framework",
            "html_url": "https://github.com/spring-projects/spring-framework",
            "owner": {"login": "spring-projects"},
            "stargazers_count": 52000,
            "description": "Spring Framework provides core support for dependency injection and more."
        },
        {
            "name": "guava",
            "html_url": "https://github.com/google/guava",
            "owner": {"login": "google"},
            "stargazers_count": 47000,
            "description": None
        }
    ]
}


class TestGitHubAPIClient(unittest.TestCase):
    @patch("Lab17_awilliams2_java.requests.get")
    def test_fetch_top_repositories(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RESPONSE

        client = GitHubAPIClient(language="Java")
        response = client.fetch_top_repositories()

        self.assertIn("items", response)
        self.assertEqual(len(response["items"]), 2)


class TestRepoDataParser(unittest.TestCase):
    def test_extract_repo_data(self):
        parser = RepoDataParser(MOCK_RESPONSE)
        repo_links, stars, labels = parser.extract_repo_data()

        self.assertEqual(len(repo_links), 2)
        self.assertTrue("spring-framework" in repo_links[0])
        self.assertEqual(stars[1], 47000)
        self.assertIn("No description provided.", labels[1])


class TestRepoPlotter(unittest.TestCase):
    def test_plot_does_not_crash(self):
        repo_links = ["<a href='url1'>Repo1</a>", "<a href='url2'>Repo2</a>"]
        stars = [123, 456]
        labels = ["owner1<br />desc1", "owner2<br />desc2"]
        plotter = RepoPlotter(repo_links, stars, labels, language="Java")

        try:
            plotter.plot()  # Will still show an empty fig in offline env
            success = True
        except Exception:
            success = False

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
