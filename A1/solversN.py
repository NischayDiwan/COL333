from re import search
from tracemalloc import start
import random

class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        self.best_state = None  
        alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self._options = {}
        for char in alpha:
            self._options[char]=[]
        for key,value in conf_matrix.items():
            for v in value:
                if key not in self._options[v]:
                    self._options[v].append(key)
        self._frontier = []

    def mult_search(self,i,max_len):
        k = len(self._frontier)
        for idx in range(k):
            state = self._frontier[idx]
            c = state[i]
            if c == ' ':
                continue
            L = self._options[c]
            for ch in L:
                temp = state[0:i]+ch+state[i+1:]
                self._frontier.append(temp)
        self._frontier.sort(key=self.cost_fn)
        if len(self._frontier) < max_len+1:
            return
        else:
            self._frontier = self._frontier[0:max_len]
            

    def search_iter(self,state,itr):
        if(itr >= 20):
            return state
        else:
            m = len(state)
            temp_best = state
            temp_min = self.cost_fn(state)
            for i in range(m):
                c = state[i]
                if c == ' ':
                    continue
                L = self._options[c]
                for ch in L:
                    temp = state[0:i]+ch+state[i+1:]
                    cost = self.cost_fn(temp)
                    if (cost < temp_min):
                        temp_best = temp
                        temp_min = cost
            self.best_state = temp_best
            return self.search_iter(temp_best,itr+1)

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        n = len(start_state)
        self.best_state = start_state
        min_cost = self.cost_fn(self.best_state)
        self._frontier = []
        self._frontier.append(start_state)
        # for i in range(n): # Attempt at using Best First Search
        #     c = self.best_state[i]
        #     if c == ' ':
        #         continue
        #     L = self.conf_matrix[c]
        #     for ch in L:
        #         temp = self.best_state[0:i]+ch+self.best_state[i+1:]
        #         if self.cost_fn(temp) < min_cost:
        #             self.best_state = temp
        #             min_cost = self.cost_fn(temp)
        # self.best_state = self.search_iter(start_state,0)
        idxs = [i for i in range(n)]
        random.shuffle(idxs)
        for i in range(n):
            self.mult_search(i,20)
        self.best_state = self._frontier[0]
        print(self.cost_fn(start_state),self.cost_fn(self.best_state))

