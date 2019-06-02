'''heuristics_option1
This file augments Wicked_Problem.py with heuristic information,
so that it can be used by an A* implementation.

The particular heuristic incorporates all the factors of a given state. 
The heuristic value returned... to ensure admissability

'''

#from Wicked_Problem import *

def h(s):
  ''' returns the number of states that have not reached their goal states '''
  goal_state_sf = [0.0204, 0.03035, 0.0269, 0.0159, 0.0278, 0.04645, 0.0242, 0.0409]
  goal_state_treatment = 0.9

  count = 0
  for i in range(8):
    if s.d[i]['sf'] < goal_state_sf[i] and s.d[i]['treatment'] > goal_state_treatment:
        count = count + 1

  return 8 - count

