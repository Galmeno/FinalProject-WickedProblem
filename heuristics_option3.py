'''heuristics_option3
This file augments Wicked_Problem.py with heuristic information,
so that it can be used by an A* implementation.

The particular heuristic incorporates all the factors that determine goal state.

'''

#from Wicked_Problem import *

def h(s):
  ''' returns the number of regions that have not reached their goal states '''
  goal_state_sf = [0.0204, 0.03035, 0.0269, 0.0159, 0.0278, 0.04645, 0.0242, 0.0409]
  goal_state_treatment = 0.9

  sum = 0
  for i in range(8):
    sfp = 1 - goal_state_sf[i] / s.d[i]['sf']
    tp = s.d[i]['treatment'] / goal_state_treatment
    sum += sfp + tp

  return sum