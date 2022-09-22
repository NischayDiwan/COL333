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

    def word_search(self,state):
        L = state.split(" ")
        x = 4
        L1 = L.copy()
        itr1 = 0
        while(itr1 <x*len(L)):
            itr = itr1 % len(L)
            if(1 > 0):
                word = L1[itr]
                m = len(word)
                temp_best = state
                temp_min = self.cost_fn(state)
                for i in range(m):
                    c = word[i]
                    O = self._options[c]
                    for ch in O:
                        temp = word[0:i]+ch+word[i+1:]
                        TempL = L.copy()
                        TempL[itr] = temp
                        temp_state = ""
                        for j in range(len(TempL)):
                            if(j == len(TempL) - 1):
                                temp_state += TempL[j]
                            else:
                                temp_state += (TempL[j] + " ")
                        cost = self.cost_fn(temp_state)
                        if cost < temp_min:
                            temp_best = temp_state
                            self.best_state = temp_best
                            temp_min = cost
                if(m > 1 and (itr1 >=len(L))):
                    i,j = 0,0
                    for i in range(0,m-1):
                        for j in range(i+1,m):
                            c = word[i]
                            c1 = word[j]
                            O = self._options[c]
                            O1 = self._options[c1]
                            for ch in O:
                                for ch1 in O1:
                                    temp = word[0:i]+ch+word[i+1:j]+ch1+word[j+1:]
                                    TempL = L.copy()
                                    TempL[itr] = temp
                                    temp_state = ""
                                    for jj in range(len(TempL)):
                                        if(jj == len(TempL) - 1):
                                            temp_state += TempL[jj]
                                        else:
                                            temp_state += (TempL[jj] + " ")
                                    cost = self.cost_fn(temp_state)
                                    if cost < temp_min:
                                        temp_best = temp_state
                                        self.best_state = temp_best
                                        temp_min = cost
                if(m > 2 and (itr1 >= 2* len(L))):
                    i,j,g = 0,0,0
                    for i in range(0,m-2):
                        for j in range(i+1,m-1):
                            for g in range(j+1,m):
                                c = word[i]
                                c1 = word[j]
                                c2 = word[g]
                                O = self._options[c]
                                O1 = self._options[c1]
                                O2 = self._options[c2]
                                for ch in O:
                                    for ch1 in O1:
                                        for ch2 in O2:
                                            temp = word[0:i]+ch+word[i+1:j]+ch1+word[j+1:g]+ch2+word[g+1:]
                                            TempL = L.copy()
                                            TempL[itr] = temp
                                            temp_state = ""
                                            for jj in range(len(TempL)):
                                                if(jj == len(TempL) - 1):
                                                    temp_state += TempL[jj]
                                                else:
                                                    temp_state += (TempL[jj] + " ")
                                            cost = self.cost_fn(temp_state)
                                            if cost < temp_min:
                                                temp_best = temp_state
                                                self.best_state = temp_best
                                                temp_min = cost
                if(m > 3 and (itr1 >= 3* len(L))):
                    i,j,g,h = 0,0,0,0
                    for i in range(0,m-3):
                        for j in range(i+1,m-2):
                            for g in range(j+1,m-1):
                                for h in range(g+1,m):
                                    c = word[i]
                                    c1 = word[j]
                                    c2 = word[g]
                                    c3 = word[h]
                                    O = self._options[c]
                                    O1 = self._options[c1]
                                    O2 = self._options[c2]
                                    O3 = self._options[c3]
                                    for ch in O:
                                        for ch1 in O1:
                                            for ch2 in O2:
                                                for ch3 in O3:
                                                    temp = word[0:i]+ch+word[i+1:j]+ch1+word[j+1:g]+ch2+word[g+1:h]+ch3+word[h+1:]
                                                    TempL = L.copy()
                                                    TempL[itr] = temp
                                                    temp_state = ""
                                                    for jj in range(len(TempL)):
                                                        if(jj == len(TempL) - 1):
                                                            temp_state += TempL[jj]
                                                        else:
                                                            temp_state += (TempL[jj] + " ")
                                                    cost = self.cost_fn(temp_state)
                                                    if cost < temp_min:
                                                        temp_best = temp_state
                                                        self.best_state = temp_best
                                                        temp_min = cost
                self.best_state = temp_best
                state = temp_best
                L = state.split(" ")
            itr1 += 1
        return state

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        n = len(start_state)
        self.best_state = start_state
        self.best_state = self.word_search(start_state)
