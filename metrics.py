from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from log import log

class Metric(ABC):
    # Base class for all metric classes. The method calculate_scores() calculates the normalized
    # scores for each metric. The abstract class calculate_score() forces all derived metric 
    # classes to provide functionality on how a metric score is calculated.

    def __init__(self, name, weight):
        self.name   = name
        self.weight = weight

    def calculate_scores(self, repositories):
        scores = []
        for repo in repositories:
            scores.append(self.calculate_score(repo))

        log.log_metric_subscores_calculated(self, scores, repositories)

        if len(scores) <= 1:
            return scores

        maxScore, minScore = max(scores), min(scores)
        for i, score in enumerate(scores):
            scores[i] = (score - minScore) / (maxScore - minScore)

        log.log_norm_metric_subscores_calculated(self, scores, repositories)
        return scores

    @abstractmethod
    def calculate_score(self, repo):
        pass

class RampUpMetric(Metric):
    def calculate_score(self, repo):
        read_me_size = len(repo.read_me.split("\n"))

        log.log_subscore_calculated(repo, read_me_size, self)
        return read_me_size

class CorrectnessMetric(Metric):
    def calculate_score(self, repo):
        score = repo.num_stars + repo.num_forks

        log.log_subscore_calculated(repo, score, self)
        return score

class BusFactorMetric(Metric):
    def calculate_score(self, repo):
        contributors = {}
        for commit in repo.commits:
            if commit.author not in contributors:
                contributors[commit.author] = 1
            else:
                contributors[commit.author] += 1

        score = len(contributors.keys())

        log.log_subscore_calculated(repo, score, self)
        return score
 
class ResponsivenessMetric(Metric):
    def calculate_score(self, repo):
        ave_time_issue_is_open = self.__get_ave_time_issue_is_open(repo)
        num_dependencies       = self.__get_num_dependencies(repo)

        score = -(ave_time_issue_is_open + num_dependencies)
        
        log.log_subscore_calculated(repo, score, self)
        return score

    def __get_ave_time_issue_is_open(self, repo):
        avg_time_issue_is_open = 0
        for issue in repo.open_issues:
            avg_time_issue_is_open += (datetime.now().day - issue.created_at.day)

        score = (avg_time_issue_is_open / len(repo.open_issues))
        return score

    def __get_num_dependencies(self, repo):
        return repo.num_dependencies

class LicenseMetric(Metric):
    def calculate_score(self, repo):
        score = 1 if repo.license_name in ['MIT', 'lgpl-2.1'] else 0
        
        log.log_subscore_calculated(repo, score, self)
        return score

    