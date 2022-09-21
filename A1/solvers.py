class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.options = {}
        for char in alpha:
            self.options[char]=[]
        for key,value in conf_matrix.items():
            for v in value:
                if key not in self.options[v]:
                    self.options[v].append(key)
        # print(self.options)
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None

    def __word_search(self,word_list):
        pass  

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        n = len(start_state)
        L = start_state.split()
        self.best_state = start_state
        min_cost = self.cost_fn(self.best_state)
        for i in range(n): # Attempt at using Best First Search
            c = self.best_state[i]
            if c == ' ':
                continue
            L = self.options[c]
            for ch in L:
                temp = self.best_state[0:i]+ch+self.best_state[i+1:]
                if self.cost_fn(temp) < min_cost:
                    self.best_state = temp
                    min_cost = self.cost_fn(temp)
        print(self.cost_fn(self.best_state))

