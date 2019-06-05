'''heuristics_option1
This file augments Wicked_Problem.py with heuristic information,
so that it can be used by an A* implementation.

The particular heuristic incorporates all the factors that determine goal state.

'''

from Wicked_Problem import *

def h(s):
  ''' returns the number of regions that have not reached their goal states '''
  goal_state_sf = [0.0204, 0.03565, 0.0367, 0.026, 0.0159]
  goal_state_treatment = 0.9

  rc = s.rc_complete
  rs = 12 - s.research_start
  sum = 0.0
  for i in range(5):
    time = s.quarter + 4 * s.year
    if(s.d[i]['sf'] > goal_state_sf[i]):
        sum += (s.d[i]['sf'] - goal_state_sf[i])
    if(s.d[i]['treatment'] < goal_state_treatment):
        sum += goal_state_treatment - s.d[i]['treatment']
  if sum != 0:
    sum = sum * 15 + rs / 2
    sum = sum / (rc * 3 + 1) - 5.545
  return sum