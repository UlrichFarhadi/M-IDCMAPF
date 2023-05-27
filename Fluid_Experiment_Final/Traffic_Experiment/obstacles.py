import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# # Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '../..'))
sys.path.append(parent_dir)


map_file = "Environments/random-32-32-20.map"
obstacles = []
with open(map_file, "r") as file:
    next(file)
    height = int(next(file).split()[1]) # get the height from the map file
    width = int(next(file).split()[1]) # get the width from the map file
    next(file)
    lines = reversed(file.readlines())
    #logging.info("Marking the obstacles in the graph")
    for y, line in enumerate(lines):
        for x, item in enumerate(line[:-1]):
            if item in ("T", "@"):
                #print(y,x, item)
                obstacles.append((x, y))
         
print(obstacles)