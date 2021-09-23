import random 
from .metric import Metric

class Dummy(Metric):
    '''
        A dummy metric that returns a random score. This random score is defined
        when an object is initialized, so that the object returns the same score
        every time caculate_score is called. This class is for testing purposes only.
    '''
    def __init__(self, name, weight):
        super().__init__(name, weight)
        self.random_score = random.random()

    def calculate_score(self, repository):
        return self.random_score