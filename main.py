import sys
import os

from github import Github

from repository import Repository
from metrics import RampUpMetric, CorrectnessMetric, BusFactorMetric, ResponsivenessMetric
from score import Score 

def create_list_of_repositories(file_name, github):
    # Accepts the file name where a list of repository urls is located. Creates a 
    # list of Repository objects from these urls and returns this list. Removes the 
    # '\n' character from the end of each line.

    repositories = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            if line[-1] == "\n":
                line = line[:-1]
            print(line)

            repo = Repository(line, github)
            repositories.append(repo)

    return repositories

if __name__ == "__main__":
    # Creates a github object used for interacting with GitHub. Creates a list of repositories
    # that will be analyzed, and a list of metrics that will be used to calculate the score. 
    # Iterates through each metric to calculate each sub score for each repository. Ranks the 
    # repositories based on the total score.
    
    token  = os.environ["GITHUB_TOKEN"]
    github = Github(token)

    repositories = create_list_of_repositories(sys.argv[1], github)
    metrics      = [
        RampUpMetric("ramp up", .1),
        CorrectnessMetric("correctness", .2),
        BusFactorMetric("bus factor", .5),
        ResponsivenessMetric("responsiveness", .3)
    ]

    scores = []
    for metric in metrics:
        metric.calculate_scores(repositories)

    scoreObject = Score(metrics)
    scores = scoreObject.get_scores(repositories)
    print(scores)
