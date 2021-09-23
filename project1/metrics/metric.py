from abc import ABC, abstractmethod

class Metric(ABC):
    '''
        An abstract class that defines the interface for all metrics. Each metric class
        that is derived from this class must have a name, a weight, and a public method
        called calculate_score.
    '''

    def __init__(self, name, weight):
        self.name   = name
        self.weight = weight

    @abstractmethod
    def calculate_score(self, repository):
        pass