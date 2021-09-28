import requests
import datetime
import os

from urllib.parse import urlparse

from github import Github

class Issue():
    def __init__(self, title, created_at):
        self.title      = title
        self.created_at = created_at

class Repository():
    # A class that provides an API for interacting with a repository stored on github.
    # Accepts a url and a github object. The github object is used to interact with the
    # github REST API. The url could either be a github url or an npm url. If it is an 
    # npm url, it is converted into a github url. When an object is initialized, fetches
    # all needed data from github. 

    def __init__(self, url, github):
        self.github = github

        self.__set_github_repo(url)

        self.name          = ""
        self.num_js_files  = 0
        self.closed_issues = 0
        self.stars         = 0
        self.pull_requests = 0
        self.forks         = 0

        # self.__fetch_coverage()
        # self.__fetch_closed_issues()
        self.__fetch_stars()
        self.__fetch_pulls()
        self.__fetch_forks()
        self.__fetch_open_issues()

    def __set_github_repo(self, url):
        url_components = urlparse(url)
        repo_url       = ""

        if 'github' in url_components[1]:            
            repo_url = url
        else:
            package_name = urlparse(url)[2].split('/package/')[1]
            url          = "https://api.npms.io/v2/package/{}".format(package_name)
            response     = requests.get(url)
            repo_url     = response.json()["collected"]['metadata']['links']['repository']

        url_components = urlparse(repo_url)
        self.repo      = self.github.get_repo(url_components[2][1:])
        self.name      = self.repo.name

    def __fetch_coverage(self):
        contents = self.repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            else:                
                if (file_content.path[len(file_content.path) - 3 : ] == ".js"):                    
                    self.num_js_files += 1
                    
    def __fetch_closed_issues(self):
        closed_issues = self.repo.get_issues(state='closed')
        # closed_issues = len(list(closed_issues))

    def __fetch_stars(self):
        self.stars = self.repo.stargazers_count

    def __fetch_pulls(self):
        pulls              = self.repo.get_pulls(state='open', sort='created', base='master')
        self.pull_requests = len(list(pulls))
        
    def __fetch_forks(self):
        self.forks = self.repo.forks_count

    def __fetch_open_issues(self):
        self.open_issues = []
        for issue in list(self.repo.get_issues(state='open')):
            self.open_issues.append(Issue(issue.title, issue.created_at))





