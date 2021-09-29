import unittest
import warnings
import os

from github import Github

from repository import Repository

class TestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        warnings.simplefilter('ignore', category=ResourceWarning)

        token       = os.environ["GITHUB_TOKEN"]
        url         = 'https://github.com/ECE-461-Group-G/test'   
        self.github = Github(token)
        self.repo   = Repository(url, self.github)

    def test_repository_name(self):
        self.assertEqual(self.repo.name, 'test')

    def test_num_starts(self):
        self.assertEqual(self.repo.num_stars, 1)
        
    def test_num_pull_requests(self):
        self.assertEqual(self.repo.num_pull_requests, 0)

    def test_num_forks(self):
        self.assertEqual(self.repo.num_forks, 0)

    def test_open_issues(self):
        self.assertEqual(len(self.repo.open_issues), 2)

    def test_commits(self):
        self.assertEqual(len(self.repo.commits), 3)
        for commit in self.repo.commits:
            self.assertEqual(commit.author, 'MDQ6VXNlcjU2NTE1Mjgz')

    def test_read_me(self):
        readme_text = "This is line #1.\n\nThis is line #3.\n"
        self.assertEqual(self.repo.read_me, readme_text)

    def test_num_dependencies(self):
        self.assertEqual(self.repo.num_dependencies, 0)

    
    