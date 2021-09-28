from datetime import datetime

from .metric import Metric

class Responsiveness(Metric):
    def calculate_score(self, repository):
        self.__find_average_time_issue_is_open(repository)

    def __find_average_time_issue_is_open(self, repository):
        for issue in repository.open_issues:
            print(datetime.now(), issue.created_at, datetime.now() - issue.created_at)