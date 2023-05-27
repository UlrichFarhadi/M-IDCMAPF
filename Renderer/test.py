# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os



# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map
import renderer

testmap = Map(10, 10)
print(testmap.map_height)
testmap.generate_map("Environments/random-32-32-10.map") # don't work for me


testrenderer = renderer.Renderer(testmap)
testrenderer.display_frame(5)


