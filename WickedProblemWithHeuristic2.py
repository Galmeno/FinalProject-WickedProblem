'''heuristics_option4
This file augments Wicked_Problem.py with heuristic information,
so that it can be used by an A* implementation.

The particular heuristic incorporates all the factors that determine goal state.
Because research is the most beneficial, as it affects all the quarters/years and regions
following it being done, funding research is the most ideal option when available.
This means, budget, cost, quarter, sf, and treatment.

'''

from Wicked_Problem import *

count = 40

def h(s):
  global count
  ''' returns the number of regions that have not reached their goal states '''
  goal_state_sf = [0.0204, 0.03565, 0.0367, 0.026, 0.0159]
  goal_state_treatment = 0.9

  # if research is being started in a state make that a higher priority
  # if the year is almost done (last quarter), gear towards the action that depletes the budget most
  # count the difference of sf and goal states and the difference of treatment and goal states

  sum = 0.0
  for i in range(5):
    if (s.d[i]['sf'] > goal_state_sf[i]):
      sum += (s.d[i]['sf'] - goal_state_sf[i])
    if (s.d[i]['treatment'] < goal_state_treatment):
      sum += goal_state_treatment - s.d[i]['treatment']

  # sum = sum * (s.year * 4 + s.quarter)
  # if s.research_start >= 0:
  #   sum = sum * (s.research_start+2)

  #sum = sum * (s.yearly_cost/28000000000)
  if s.year == 0 and s.quarter == 1:
    count = 0
    for i in range(5):
      val1 = s.d[i]['sf']
      val2 = s.d[i]['treatment']
      while val1 > goal_state_sf[i] or val2 < goal_state_treatment:
        val1 = val1 * 0.7
        val2 = val2 * 1.2
        count = count + 1
  if(goal_test(s)):
    return 0
  return (count - s.year * 4 - s.quarter) + (sum) + 5.0
