cases = 36900000
sf = 0.0488
deaths = 940000
time = 0

regions = {0 : 'East and Southern Africa', 1 : 'Western and Central Africa', 2 : 'Asia and Pacific', 3 : 'Western and Central Europe and North America', \
    4 : 'Latin America', 5 : 'Eastern Europe and Central Asia', 6 : 'Carribean', 7 : 'Middle East and North Africa'}

init_dict = {0: {'cases' : 19600000, 'sf' : 0.0408, 'deaths' : 426666, 'treatment' : 0.66}, 1 : {'cases' : 6100000, 'sf' : 0.0607, 'deaths' : 197333, 'treatment' : 0.40}, \
    2 : {'cases' : 5200000, 'sf' : 0.0538, 'deaths' : 149333, 'treatment' : 0.53}, 3 : {'cases' : 2200000, 'sf' : 0.0318, 'deaths' : 37351, 'treatment' : 0.76}, \
    4 : {'cases' : 1800000, 'sf' : 0.0556, 'deaths' : 53329, 'treatment' : 0.61}, 5 : {'cases' : 1400000, 'sf' : 0.0929, 'deaths' : 69334, 'treatment' : 0.36}, \
    6 : {'cases' : 310000, 'sf' : 0.0484, 'deaths' : 8000, 'treatment' : 0.57}, 7 : {'cases' : 220000, 'sf' : 0.0818, 'deaths' : 9600, 'treatment' : 0.29}}

CREATE_INITIAL_STATE = lambda: State(init_dict, 0)


class State:
    def __init__(self, d, time):
        self.d = d
        self.time = time

    def __eq__(self, s2):
        for i in range(8):
            for j in ['cases', 'sf', 'death', 'treatment']:
                if self.d[i][j] != s2.d[i][j]:
                    return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        s = 'Time from start: ' + str(self.time) + ' months. \n'
        for i in range(8):
            s += regions[i] + ': ' + str(self.d['cases']) + ' cases, ' + str(self.d['sf']) + ' spreading factor, ' + \
                str(self.d['deaths']) + ' deaths, ' + str(self.d['treatment']) + ' percent receiving treatment. \n'
        return s

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        newd = {}
        for i in range(8):
            newd[i] = {'cases' : self.d[i]['cases'], 'sf' : self.d[i]['sf'], 'deaths' : self.d[i]['deaths'], 'treatment' : self.d[i]['treatment']}
        newt = self.time
        return State(newd, newt)

    def can_move(self, b):
        pass

    def move(self, b):
        pass


def goal_test(s):
    pass


def goal_message(s):
    pass


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)