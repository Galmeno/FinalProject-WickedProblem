#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Wicked Problem: HIV/AIDS"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['H. Kaushik']
PROBLEM_CREATION_DATE = "29-MAY-2019"
PROBLEM_DESC=\
'''
This formulation of the wicked problem of disease (with a focus on HIV/AIDS)
uses generic Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.

Int_Solve_Client can  be used such that the user can choose an action among 
valid operations.
'''

BUDGET = 28000000000

# 8 Regions considered
REGIONS = {0 : 'East and Southern Africa', 1 : 'Western and Central Africa', 2 : 'Asia and Pacific', 3 : 'Western and Central Europe and North America', \
    4 : 'Latin America', 5 : 'Eastern Europe and Central Asia', 6 : 'Carribean', 7 : 'Middle East and North Africa', 8 : 'a cure', 9 : 'budgetary reasons.'}

# Dictionary of conditions relating to HIV/AIDS based on regions
INIT_DICT = {0: {'cases' : 19600000, 'sf' : 0.0408, 'deaths' : 426666, 'treatment' : 0.66}, 1 : {'cases' : 6100000, 'sf' : 0.0607, 'deaths' : 197333, 'treatment' : 0.40}, \
    2 : {'cases' : 5200000, 'sf' : 0.0538, 'deaths' : 149333, 'treatment' : 0.53}, 3 : {'cases' : 2200000, 'sf' : 0.0318, 'deaths' : 37351, 'treatment' : 0.76}, \
    4 : {'cases' : 1800000, 'sf' : 0.0556, 'deaths' : 53329, 'treatment' : 0.61}, 5 : {'cases' : 1400000, 'sf' : 0.0929, 'deaths' : 69334, 'treatment' : 0.36}, \
    6 : {'cases' : 310000, 'sf' : 0.0484, 'deaths' : 8000, 'treatment' : 0.57}, 7 : {'cases' : 220000, 'sf' : 0.0818, 'deaths' : 9600, 'treatment' : 0.29}}

CREATE_INITIAL_STATE = lambda: State(INIT_DICT, 0, 0, 0, -1)

action_costs = {'Research' : 12000000000, 'Drugs' : 8000000000, 'Education' : 6000000000, 'nothing' : 0}

class State:
    def __init__(self, d, q, y, yc, rs):
        self.d = d
        self.quarter = q
        self.year = y
        self.yearly_cost = yc
        self.research_start = rs

    def __eq__(self, s2):
        for i in range(8):
            for j in ['cases', 'sf', 'deaths', 'treatment']:
                if self.d[i][j] != s2.d[i][j]:
                    return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        s = 'Time from start: ' + str(self.quarter + 4 * self.year) + ' quarters. \n'
        if self.research_start != -1: s += 'Research in progress.\n'
        s += '$' + str(BUDGET - self.yearly_cost) + ' left to invest this year.\n'
        for i in range(8):
            s += REGIONS[i] + ': ' + str(self.d[i]['cases']) + ' cases, ' + str(self.d[i]['sf']) + ' spreading factor, ' + \
                str(self.d[i]['deaths']) + ' deaths, ' + str(self.d[i]['treatment']) + ' percent receiving treatment. \n'
        return s

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        newd = {}
        for i in range(8):
            newd[i] = {'cases' : self.d[i]['cases'], 'sf' : self.d[i]['sf'], 'deaths' : self.d[i]['deaths'], 'treatment' : self.d[i]['treatment']}
        return State(newd, self.quarter, self.year, self.yearly_cost, self.research_start)

    def can_move(self, a, loc):
        try:
            yc = self.yearly_cost
            if self.quarter == 4:
                yc = 0
            if self.research_start != -1 and a == 'Research':
                return False
            if(action_costs[a] + yc <= BUDGET):
                return True
            else: 
                return False
        except Exception as e:
            print(e)


    def move(self, a, loc):
        news = self.copy()
        news.quarter += 1
        if(news.quarter == 5):
            news.year += 1
            news.quarter = 1
            news.yearly_cost = 0
        if news.research_start != -1 and (news.year * 4 + news.quarter) - news.research_start > 12:
            for i in range(8):
                news.d[i]['deaths'] = int(self.d[i]['deaths'] * 0.8)
                news.d[i]['cases'] = int(self.d[i]['cases'] * 0.9)
                news.d[i]['sf'] = round(self.d[i]['sf'] * 0.9, 4)
            
        if a == 'Research':
            news.research_start = news.year * 4 + news.quarter
            news.yearly_cost += action_costs['Research']
            
        elif a == 'Drugs':
            news.d[loc]['deaths'] = int(self.d[loc]['deaths'] * 0.95)
            news.d[loc]['treatment'] = round(self.d[loc]['treatment'] * 1.2, 3)
            news.yearly_cost += action_costs['Drugs']
            #exit(0)
        elif a == 'Education':
            news.d[loc]['sf'] = round(self.d[loc]['sf'] * 0.9, 4)
            news.d[loc]['treatment'] = round(self.d[loc]['treatment'] * 1.1, 3)
            news.d[loc]['cases'] = int(self.d[loc]['cases'] * 0.9)
            news.yearly_cost += action_costs['Education']
            #exit(0)
        return news

            


def goal_test(s):
    for i in range(8):
        if s.d[i]['treatment'] < 0.9:
            return False
        if s.d[i]['sf'] / INIT_DICT[i]['sf'] > 0.5:
            return False
    return True


def goal_message(s):
    return 'The initial goal of HIV/AIDS prevention is reached.'


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

actions = ['Research', 'Drugs', 'Education']
combinations = [('Research', 8), ('nothing', 9)]
for a in ['Drugs', 'Education']:
    for i in range(8):
        combinations.append((a, i))

OPERATORS = [Operator('Invest in ' + a + ' for ' + REGIONS[loc] + ' ($' + str(action_costs[a]) + ')',
                      lambda s,a1=a,l1=loc: s.can_move(a1, l1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,a1=a,l1=loc: s.move(a1, l1) )
             for (a,loc) in combinations]

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)