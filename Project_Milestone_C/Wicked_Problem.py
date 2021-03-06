# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Wicked Problem: HIV/AIDS"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['H. Kaushik', 'L. Qing']
PROBLEM_CREATION_DATE = "29-MAY-2019"
PROBLEM_DESC = \
    '''
    This formulation of the wicked problem of disease (with a focus on HIV/AIDS)
    uses generic Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.

    Int_Solve_Client can  be used such that the user can choose an action among
    valid operations.
    '''

BUDGET = 28000000000

# 8 Regions considered
REGIONS = {0: 'East and Southern Africa', 1: 'Western, Central, North Africa and Middle East', 2: 'Eastern Europe and Asia',
           3: 'Western and Central Europe and North America', \
           4: 'Latin America and Carribean', 5: 'new treatment', 6: 'budgetary reasons.'}

# Dictionary of conditions relating to HIV/AIDS based on regions
INIT_DICT = {0: {'cases': 19600000, 'sf': 0.0408, 'deaths': 426666, 'treatment': 0.66}, \
             1: {'cases': 6320000, 'sf': 0.0713, 'deaths': 206933, 'treatment': 0.345}, \
             2: {'cases': 6600000, 'sf': 0.0734, 'deaths': 218667, 'treatment': 0.445}, \
             3: {'cases': 2110000, 'sf': 0.0520, 'deaths': 61329, 'treatment': 0.59}, \
             4: {'cases': 2200000, 'sf': 0.0318, 'deaths': 37351, 'treatment': 0.76}}
             

CREATE_INITIAL_STATE = lambda: State(INIT_DICT, 1, 0, 0, -1, 0)

action_costs = {'Research': 12000000000, 'Drugs': 8000000000, 'Education': 6000000000, 'nothing': 0}


class State:
    def __init__(self, d, q, y, yc, rs, rc):
        self.d = d
        self.quarter = q
        self.year = y
        self.yearly_cost = yc
        self.research_start = rs
        self.rc_complete = rc

    def __eq__(self, s2):
        for i in range(5):
            for j in ['cases', 'sf', 'deaths', 'treatment']:
                if self.d[i][j] != s2.d[i][j]:
                    return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        s = 'Year: ' + str(self.year) + ' Quarter: ' + str(self.quarter) + '. \n'
        if self.research_start != -1:
            s += 'Research in progress for ' + str(self.research_start) + ' quarters.\n'
        if self.rc_complete > 0:
            s += str(self.rc_complete) + ' research cycle(s) complete.\n'
        s += '$' + str(BUDGET - self.yearly_cost) + ' left to invest this year.\n'
        for i in range(5):
            s += REGIONS[i] + ': ' + str(self.d[i]['cases']) + ' cases, ' + str(
                self.d[i]['sf']) + ' spreading factor, ' + \
                 str(self.d[i]['deaths']) + ' deaths, ' + str(
                self.d[i]['treatment']) + ' percent receiving treatment. \n'
        return s

    def __hash__(self):
        return (self.__str__()).__hash__()

    def edge_distance(self, s2):
        return 1.0

    def copy(self):
        newd = {}
        for i in range(5):
            newd[i] = {'cases': self.d[i]['cases'], 'sf': self.d[i]['sf'], 'deaths': self.d[i]['deaths'],
                       'treatment': self.d[i]['treatment']}
        return State(newd, self.quarter, self.year, self.yearly_cost, self.research_start, self.rc_complete)

    def can_move(self, a, loc):
        try:
            yc = self.yearly_cost
            if self.research_start != -1 and a == 'Research':
                return False
            if action_costs[a] + yc <= BUDGET:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def move(self, a, loc):
        news = self.copy()
        news.quarter += 1
        if news.quarter == 5:
            news.year += 1
            news.quarter = 1
        if news.quarter == 1:
            news.yearly_cost = 0
        if news.research_start > -1:
            news.research_start += 1
        if news.research_start == 8:
            news.research_start = -1
            news.rc_complete += 1
        if news.rc_complete > 0:
            for i in range(5):
                news.d[i]['deaths'] = int(self.d[i]['deaths'] * 0.8)
                news.d[i]['cases'] = int(self.d[i]['cases'] * 0.9)
                news.d[i]['sf'] = round(self.d[i]['sf'] * (1.0 - 0.1 * news.rc_complete), 4)

                if news.d[i]['sf'] > 1:
                    news.d[loc]['sf'] = 0.999

        if a == 'Research':
            news.research_start = 0
            news.yearly_cost += action_costs['Research']

        elif a == 'Drugs':
            news.d[loc]['deaths'] = int(self.d[loc]['deaths'] * 0.9)
            news.d[loc]['treatment'] = round(self.d[loc]['treatment'] * 1.3, 3)
            news.d[loc]['sf'] = round(self.d[loc]['sf'] * 0.8, 4)
            news.yearly_cost += action_costs['Drugs']
            # exit(0)
        elif a == 'Education':
            news.d[loc]['sf'] = round(self.d[loc]['sf'] * 0.7, 4)
            news.d[loc]['treatment'] = round(self.d[loc]['treatment'] * 1.1, 3)
            news.d[loc]['cases'] = int(self.d[loc]['cases'] * 0.9)
            news.yearly_cost += action_costs['Education']
            # exit(0)

        if loc < 5:
            if news.d[loc]['sf'] > 1:
                news.d[loc]['sf'] = 0.999

            if news.d[loc]['treatment'] > 1:
                news.d[loc]['treatment'] = 0.999

        for i in range(5):
            if news.d[i]['sf'] > 0:
                news.d[i]['cases'] += int(news.d[i]['cases'] * news.d[i]['sf'])
                news.d[i]['cases'] -= news.d[i]['deaths']

        return news


def goal_test(s):
    for i in range(5):
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
combinations = [('Research', 5), ('nothing', 6)]
for a in ['Drugs', 'Education']:
    for i in range(5):
        combinations.append((a, i))

OPERATORS = [Operator('Invest in ' + a + ' for ' + REGIONS[loc] + ' ($' + str(action_costs[a]) + ')',
                      lambda s, a1=a, l1=loc: s.can_move(a1, l1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, a1=a, l1=loc: s.move(a1, l1))
             for (a, loc) in combinations]

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)