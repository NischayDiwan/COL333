from re import search
from tracemalloc import start


class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None  

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        n = len(start_state)
        self.best_state = start_state
        min_cost = self.cost_fn(self.best_state)
        # for i in range(n): Attempt at using Best First Search
            # c = self.best_state[i]
            # if c == ' ':
            #     continue
            # L = self.conf_matrix[c]
            # for ch in L:
            #     temp = self.best_state[0:i]+ch+self.best_state[i+1:]
            #     if self.cost_fn(temp) < min_cost:
            #         self.best_state = temp
            #         min_cost = self.cost_fn(temp)
        temp_best = start_state
        temp_min = min_cost
        A = []
        for i in range(n):
            c = start_state[i]
            if c == ' ':
                continue
            L = self.conf_matrix[c]
            for ch in L:
                temp = temp_best[0:i]+ch+temp_best[i+1:]
                cost = self.cost_fn(temp)
                if cost < temp_min:
                    temp_best = temp
                    temp_min = cost
        print(self.cost_fn(self.best_state))

