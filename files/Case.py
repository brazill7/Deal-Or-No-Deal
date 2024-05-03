import random as rand
class Case:
    def __init__(self, number, value):
        self.number = number
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

def generate_cases():
        '''
        Creates and randomizes the cases with predetermined values for the game.
        Each case is an instance of Case class, and their value is initialized here.
        Returns a list of Case objects.

        '''
        case_values = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750,
                       1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000,
                       300000, 400000, 500000, 750000, 1000000]
        #rand.shuffle(case_values)
        cases = [Case(i, value) for i, value in enumerate(case_values, start=1)]

        return cases
