import sys
import os

from github import Github

from repository import Repository

def create_list_of_repositories(file_name, github):
	# Accepts the file name where a list of repository urls is located.
	# Creates a list of Repository objects from these urls and returns
	# this list. Removes the '\n' character from the end of each line.

	repositories = []
	with open(file_name, "r") as file:
		for line in file.readlines():
			if line[-1] == "\n":
				line = line[:-1]

			repo = Repository(line, github)
			repositories.append(repo)

	return repositories

if __name__ == "__main__":
	token  = os.environ["GITHUB_TOKEN"]
	github = Github(token)

	repo = github.get_repo('cloudinary/cloudinary_npm')

	repositories = create_list_of_repositories(sys.argv[1], github)

