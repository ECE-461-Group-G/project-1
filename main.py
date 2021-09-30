import sys
import os

from github import Github

from repository import Repository
from metrics import LicenseMetric, RampUpMetric, CorrectnessMetric, BusFactorMetric, ResponsivenessMetric
from score import Score 
from log import log

def clear_log_file():
    log_file = os.environ['LOG_FILE']
    with open(log_file, "w") as file:
        file.write("")

def create_list_of_repositories(file_name, github):
    # Accepts the file name where a list of repository urls is located. Creates a 
    # list of Repository objects from these urls and returns this list. Removes the 
    # '\n' character from the end of each line.

    repositories = []
    with open(file_name, "r") as file:
        log.log_url_file_read(file_name)
        for line in file.readlines():
            if line[-1] == "\n":
                line = line[:-1]
            print(line)

            repo = Repository(line, github)
            repositories.append(repo)

    log.log_url_file_closed(file_name)
    log.log_repo_list_created(repositories)
    return repositories

if __name__ == "__main__":
    # Creates a github object used for interacting with GitHub. Creates a list of repositories
    # that will be analyzed, and a list of metrics that will be used to calculate the score. 
    # Iterates through each metric to calculate each sub score for each repository. Ranks the 
    # repositories based on the total score.
    clear_log_file()

    token  = os.environ["GITHUB_TOKEN"]
    github = Github(token)

    repositories = create_list_of_repositories(sys.argv[1], github)
    metrics      = [
        RampUpMetric("ramp up", .1),
        CorrectnessMetric("correctness", .2),
        BusFactorMetric("bus factor", .5),
        ResponsivenessMetric("responsiveness", .3),
        LicenseMetric("license", .9)
    ]
    log.log_metrics_created(metrics)

    for metric in metrics:
        sub_scores = metric.calculate_scores(repositories)
        for i, sub_score in enumerate(sub_scores):
            repositories[i].scores.append(sub_score)

    scoreObject = Score(metrics)
    scores      = scoreObject.get_scores(repositories)

    log.log_final_scores(scores)