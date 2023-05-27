# Library imports
import networkx as nx
import sys
import os
import copy
import networkit as nk
import numpy as np
from scipy.interpolate import interp2d
import math

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map 

class Map_directed(Map):
    def __init__(self):
        super().__init__()
    

    def generate_map(self, map_file: str):
        """
        open a .map environment and return a graph with the obstacles marked
        """

        self.current_map_file = map_file # maybe extend code to check if the path is correct
        with open(map_file, "r") as file:
            next(file)
            height = int(next(file).split()[1]) # get the height from the map file
            width = int(next(file).split()[1]) # get the width from the map file
            self.map_height = height
            self.map_width = width
            next(file)
            lines = reversed(file.readlines())
            my_map: nx.DiGraph = nx.DiGraph()
            for x in range(0, width):
                for y in range(0, height):
                    my_map.add_node((x, y))
                    my_map.nodes[(x, y)]["agent"] = None
                    
                    if x > 0:
                        my_map.add_edge((x - 1, y), (x, y), weight = 1.0)
                        my_map.add_edge((x, y),(x - 1, y) , weight = 1.0)
                    if y > 0:
                        my_map.add_edge((x, y - 1), (x, y), weight = 1.0) 
                        my_map.add_edge((x, y),(x, y - 1) , weight = 1.0) 

            
            for y, line in enumerate(lines):
                for x, item in enumerate(line[:-1]):
                    if item in ("T", "@"):
                        #print(y,x, item)
                        my_map.remove_node((x, y))
                        my_map.add_node((x, y))
                        my_map.nodes[(x, y)]["obstacle"] = True
                    else:
                        self.free_nodes.append((x, y))        

        self.map = my_map

        self.G_nk = nk.nxadapter.nx2nk(self.map, weightAttr='weight')
        self.nk_node_id = dict((id, u) for (id, u) in zip(self.map.nodes(), range(self.map.number_of_nodes())))
        self.nk_reverse_node_id = dict((u, id) for (id, u) in zip(self.map.nodes(), range(self.map.number_of_nodes())))
        self.nk_heuristic = [0 for _ in range(self.G_nk.upperNodeIdBound())]

    def update_weight_on_map(self, weight_list):

        # create a dictionary of edge attributes
        edge_attrs = {}
        for i, (x, y) in enumerate(self.map.edges()):
            edge_attrs[(x, y)] = {'weight': weight_list[i]}

        nx.set_edge_attributes(self.map, edge_attrs)
        #DEBUG
        #print(self.map.edges(data=True))

    def bicubic_interpolation(self, grid, w, q):
        grid = np.array(grid)
        n, m = grid.shape
        
        # Define the x and y coordinates of the original grid
        x = np.arange(m)
        y = np.arange(n)
        
        # Create an interpolation function using bicubic interpolation
        interp_func = interp2d(x, y, grid, kind='cubic')
        
        # Define the x and y coordinates of the output grid
        x_new = np.linspace(0, m-1, q)
        y_new = np.linspace(0, n-1, w)
        
        # Evaluate the interpolation function at the coordinates of the output grid
        output_grid = interp_func(x_new, y_new)
        output_grid = np.maximum(output_grid, 0)    # Remove all negative values
        output_grid = np.minimum(1, output_grid)
        return output_grid.tolist()

    def update_weight_on_map_by_node(self, weight_list):


        interp_grid = self.bicubic_interpolation(weight_list, w=self.map_height, q=self.map_width)

        # create a dictionary of edge attributes
        edge_attrs = {}
        for x in range(self.map_width):
            for y in range(self.map_height):
                for edge in self.map.in_edges((x, (self.map_height - 1) - y)):
                    edge_attrs[edge] = {'weight' : interp_grid[y][x]}
        
        nx.set_edge_attributes(self.map, edge_attrs)
        
        # for i, (x, y) in enumerate(self.map.edges()):
        #     edge_attrs[(x, y)] = {'weight': weight_list[i]}

    def angle_difference(self, angle1, angle2):
        # Calculate the absolute difference between the angles
        diff = abs(angle1 - angle2)
        
        # Normalize the difference to the range [0, 2*pi)
        diff = diff % (2*math.pi)
        
        # If the difference is greater than pi, subtract 2*pi to get the smaller angle
        if diff > math.pi:
            diff = 2*math.pi - diff
        
        # Return the normalized difference between 0 and 1
        return diff / math.pi

    def update_weight_on_map_by_directional(self, list_of_direction):
        edge_attrs = {}
        for idx, i in enumerate(self.free_nodes):
            idx = idx * 2
            # get edge in node
            edges_from_node = self.map.out_edges(i)

            for edge in edges_from_node:
                #get direction
                x1, y1 = edge[0]
                x2, y2 = edge[1]
                dx, dy = x2 - x1, y2 - y1
                # calculate weight for each edge based upon the direction
                angle = math.atan2(dy, dx)
                # to edge_attrs
                edge_attrs[edge] = {'weight' : self.angle_difference(angle, math.radians(list_of_direction[idx]*360))*list_of_direction[idx+1]}
        nx.set_edge_attributes(self.map, edge_attrs)

    def get_weight_list(self):
        list_of_edge_weights = []
        for x, y, w in self.map.edges.data("weight", -1): #If weight don't exists return -1 as default
            list_of_edge_weights.append(w)
        return list_of_edge_weights