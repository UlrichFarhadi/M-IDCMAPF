# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map
#from Map.map import * # Dårlig kodeskik at importere en hel fil


class Agent:
    def __init__(self, map: Map):
        self.position = None # Node_tag
        self.target = None # Node_tag
        self.path = []
        self.map = map
        self.color =(random.randint(40,205)/255, random.randint(40,205)/255, random.randint(40,205)/255)
        
    def move(self):
        # get current position and next position from path
        # Returns false if the agent has reached the goal
        if len(self.path) == 0:
            self.map.update_agent_on_map(self, self.target, self.target)
            return False
        
        pos_prev = self.position
        pos_next = self.path.pop(0)
        
        # check for collision and apply the 7 rules
        # update the position accordingly
        # ...
        
        # update agent position on the map
        self.map.update_agent_on_map(self, pos_prev, pos_next)
        self.position = pos_next
