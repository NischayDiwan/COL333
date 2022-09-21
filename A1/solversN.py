from re import search
from tracemalloc import start
import random
from warnings import resetwarnings

class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self._options = {}
        for char in alpha:
            self._options[char]=[]
        for key,value in conf_matrix.items():
            for v in value:
                if key not in self._options[v]:
                    self._options[v].append(key)
        # print(self.options)
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        self.best_state = None
        self._frontier = []
        self._frontier_size = 20

    def local_beam_search(self,i):
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
        if len(self._frontier) <= self._frontier_size:
            return
        else:
            L = []
            for u in range(self._frontier_size//2):
                L.append(self._frontier.pop(0))
            it = 0
            p = 0.9
            n = len(self._frontier)
            while len(L)<self._frontier_size:
                r = random.uniform(0.0,1.0)
                elem = self._frontier.pop(0)
                if r<=p:
                    L.append(elem)
                else:
                    self._frontier.append(elem)
                it+=1
                p*=0.9
                if it == n:
                    it = 0
                    p = 0.9
                    n = len(self._frontier)
            self._frontier = L
            

    def search_iter(self,state,itr):

        # Aproach 3
        # L = state.split(" ")
        # if(itr == len(L)):
        #     return state
        # else:
        #     m = len(L[itr])
        #     # print(m)
        #     word = L[itr]
        #     temp_best = state
        #     temp_min = self.cost_fn(state)
        #     for i in range(m):
        #         c = L[itr][i]
        #         # if c == ' ':
        #         #     continue
        #         O = self.options[c]
        #         for ch in O:
        #             temp = word[0:i]+ch+word[i+1:]
        #             TempL = L.copy()
        #             TempL[itr] = temp
        #             temp_state = ""
        #             for j in range(len(TempL)):
        #                 temp_state += (TempL[j] + " ")
        #             cost = self.cost_fn(temp_state)
        #             if cost < temp_min:
        #                 temp_best = temp_state
        #                 temp_min = cost
        #     self.best_state = temp_best
        #     return self.search_iter(temp_best,itr+1)

        # Approch 2
        # if(itr >= 20):
        #     return state
        # else:
        #     m = len(state)
        #     temp_best = state
        #     temp_min = self.cost_fn(state)
        #     for i in range(m):
        #         c = state[i]
        #         if c == ' ':
        #             continue
        #         L = self.options[c]
        #         for ch in L:
        #             temp = state[0:i]+ch+state[i+1:]
        #             cost = self.cost_fn(temp)
        #             if cost < temp_min:
        #                 temp_best = temp
        #                 temp_min = cost
        #     self.best_state = temp_best
        #     return self.search_iter(temp_best,itr+1)

        if(itr >= 20):
            return state
        else:
            m = len(L[itr])
            # print(m)
            word = L[itr]
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
        for i in range(n):
            self.local_beam_search(i,self._frontier_size)
        self.best_state = self._frontier[0]
        print(self.cost_fn(start_state),self.cost_fn(self.best_state))
