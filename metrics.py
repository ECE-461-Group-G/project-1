from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Metric(ABC):
    # Base class for all metric classes. The method calculate_scores() calculates the normalized
    # scores for each metric. These scores are than saved to each repository's score list. The
    # abstract class calculate_score() forces all derived metric classes to provide functionality
    # on how a metric score is calculated.

    def __init__(self, name, weight):
        self.name   = name
        self.weight = weight

    def calculate_scores(self, repositories):
        scores = []
        for repo in repositories:
            scores.append(self.calculate_score(repo))

        if len(scores) <= 1:
            return scores

        maxScore = max(scores)
        minScore = min(scores)
        for i, score in enumerate(scores):
            norm_score = (score - minScore) / (maxScore - minScore)
            repositories[i].scores.append(norm_score)

    @abstractmethod
    def calculate_score(self, repo):
        pass

class RampUpMetric(Metric):
    def calculate_score(self, repo):
        read_me_size = len(repo.read_me.split("\n"))
        return read_me_size

class CorrectnessMetric(Metric):
    def calculate_score(self, repo):
        return repo.num_stars + repo.num_forks

class BusFactorMetric(Metric):
    def calculate_score(self, repo):
        contributors = {}
        for commit in repo.commits:
            if commit.author not in contributors:
                contributors[commit.author] = 1
            else:
                contributors[commit.author] += 1
        
        return len(contributors.keys())
 
class ResponsivenessMetric(Metric):
    def calculate_score(self, repo):
        num_contributors = self.__get_num_active_contributers(repo)
        num_dependencies = self.__get_num_dependencies(repo)

        return 2.0 * num_contributors - .5 * num_dependencies

    def __get_num_active_contributers(self, repo):
        avg_time_issue_is_open = 0
        for issue in repo.open_issues:
            avg_time_issue_is_open += datetime.now().timestamp() - issue.created_at.timestamp()

        return avg_time_issue_is_open / len(repo.open_issues)

    def __get_num_dependencies(self, repo):
        return repo.num_dependencies

    