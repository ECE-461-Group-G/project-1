import unittest

from project1.score import Score
from project1.metrics.dummy import Dummy
from ..repository import Repository

class TestScores(unittest.TestCase):
    def test_score(self):
        '''
            The Score object should calculate the correct total score for an individual
            repository. This total score is calculated by finding the weighted sum of all
            sub scores. 
        '''
        repository = Repository()
        metrics    = [
            Dummy('metric1', .5),
            Dummy('metric2', .3),
            Dummy('metric3', .8)
        ]

        scoreObject = Score([repository], metrics)
        score       = scoreObject.get_scores()[0]['score']

        desiredScore = 0
        for metric in metrics:
            desiredScore += metric.weight * metric.calculate_score(repository)

        self.assertEqual(score, desiredScore)

    def test_ordered_scores(self):
        '''
            The Score object should return a list of repositories sorted by their total score (in
            descending order).
        '''
        repositories = [
            Repository(),
            Repository(),
            Repository(),
            Repository(),
            Repository(),
        ]
        metrics = [
            Dummy('metric1', .1),
            Dummy('metric2', .2),
            Dummy('metric3', .3)
        ]

        scoreObject = Score(repositories, metrics)
        scores      = scoreObject.get_scores()

        for i in range(1, len(scores)):
            self.assertTrue(scores[i]['score'] <= scores[i - 1]['score'])