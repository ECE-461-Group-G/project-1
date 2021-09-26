from .repository import Repository

class Node:
    # Used to contain scoring information for a repository. Also has a left and right child
    # for use in a binary tree.
    
    def __init__(self, repository, score, sub_scores):
        self.repository = repository
        self.score      = score
        self.sub_scores = sub_scores

        self.left       = None
        self.right      = None

    def to_dict(self):
        return {
            'repository': self.repository, 
            'score':      self.score, 
            'sub_scores': self.sub_scores
        }

class Score:
    # When a score object is created, a list of repositories and a list of metrics is passed
    # to it's constructor. The purpose of this object is to calculate the sub scores and total
    # score for each repository, and returns an list of these repositories ordered by their
    # total score (in descending order). Uses a binary tree to store the scores.

    def __init__(self, repositories, metrics):
        self.repositories = repositories
        self.metrics      = metrics
        self.tree         = None

    def get_scores(self):
        for repository in self.repositories:
            score, sub_scores = self.__get_scores(repository)
            node              = Node(repository, score, sub_scores)
            self.__insert_into_tree(self.tree, node)

        return self.__get_ordered_list(self.tree)

    def __get_scores(self, repository):
        score      = 0
        sub_scores = []
        for metric in self.metrics:
            sub_score = metric.calculate_score(repository)
            score    += sub_score * metric.weight
            sub_scores.append(sub_score)

        return score, sub_scores

    def __insert_into_tree(self, tree, node):
        if self.tree is None:
            self.tree = node
            return

        if node.score < tree.score:
            if tree.right is None:
                tree.right = node
            else:
                self.__insert_into_tree(tree.right, node)
        else:
            if tree.left is None:
                tree.left = node
            else:
                self.__insert_into_tree(tree.left, node)

    def __get_ordered_list(self, tree):
        if tree is None:
            return

        ordered_list = []

        left_list = self.__get_ordered_list(tree.left)
        if left_list is not None:
            ordered_list += left_list

        ordered_list.append(tree.to_dict())

        right_list = self.__get_ordered_list(tree.right)
        if right_list is not None:
            ordered_list += right_list

        return ordered_list

