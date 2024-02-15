import random

class randomFiarAgent:

    def __init__(self, env, seed = None):
        self._random = random.Random()
        self.env = env
        if(seed != None):
            self._random.seed(seed)

    def filterCol(self, el):
            return self.env.column_height(el) != self.env.rows

    def select_col(self):

        available_rows = list(filter(self.filterCol, range(0, self.env.columns)))
        
        return self._random.choice(available_rows)

    