'''heuristics_option4
This file augments Wicked_Problem.py with heuristic information,
so that it can be used by an A* implementation.

The particular heuristic incorporates all the factors that determine goal state.
Because research is the most beneficial, as it affects all the quarters/years and regions 
following it being done, funding research is the most ideal option when available. 
This means, budget, cost, quarter, sf, and treatment.

'''

from Wicked_Problem import *

def h(s):
  ''' returns the number of regions that have not reached their goal states '''
  goal_state_sf = [0.0204, 0.03035, 0.0269, 0.0159, 0.0278, 0.04645, 0.0242, 0.0409]
  goal_state_treatment = 0.9

  mult = 0.5

  # Need to check only for start - not while it is conducting.
  if s.research_start == 1:
      # if research is an option, we want to fund research.
      mult = 1

  sum = 0
  
  for i in range(8):
    sfp = 1 - goal_state_sf[i] / s.d[i]['sf']
    tp = s.d[i]['treatment'] / goal_state_treatment
    sum += sfp + tp

  sum = sum * mult 
  return sum