import sys
import os

from github import Github

from repository import Repository
from metrics.responsiveness import Responsiveness

def create_list_of_repositories(file_name, github):
	# Accepts the file name where a list of repository urls is located. Creates a 
	# list of Repository objects from these urls and returns this list. Removes the 
	# '\n' character from the end of each line.

	repositories = []
	with open(file_name, "r") as file:
		for line in file.readlines():
			print(line)
			if line[-1] == "\n":
				line = line[:-1]

			repo = Repository(line, github)
			repositories.append(repo)

	return repositories

if __name__ == "__main__":
	token  = os.environ["GITHUB_TOKEN"]
	github = Github(token)

	repositories   = create_list_of_repositories(sys.argv[1], github)
	responsiveness = Responsiveness('responsiveness', 1.0)
	
	# for repo in repositories:
	# 	print("\n ---- New Repository ---- \n")
	# 	responsiveness.calculate_score(repo)


