# Library imports
import networkx as nx
import sys
import os
import copy
import networkit as nk

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

class Map:
    """
    ask ChatGPT to generate a docstring describing every class! when the class is finished and no more implementations are needed.
    """
    def __init__(self):
        self.map = nx.Graph()
        self.map_height = None
        self.map_width = None
        self.current_map_file: str = None
        self.free_nodes = []
        self.map_name = ""
        
    def generate_map(self, map_file: str):
        """
        open a .map environment and return a graph with the obstacles marked
        """
        file_name_with_ext = os.path.basename(map_file)
        self.map_name = os.path.splitext(file_name_with_ext)[0]
        self.current_map_file = map_file # maybe extend code to check if the path is correct
        with open(map_file, "r") as file:
            next(file)
            height = int(next(file).split()[1]) # get the height from the map file
            width = int(next(file).split()[1]) # get the width from the map file
            self.map_height = height
            self.map_width = width
            next(file)
            lines = reversed(file.readlines())
            my_map: nx.Graph = nx.Graph()
            for x in range(0, width):
                for y in range(0, height):
                    my_map.add_node((x, y))
                    my_map.nodes[(x, y)]["agent"] = None
                    # logging.info(f"Adding {x} and {y}")
                    if x > 0:
                        my_map.add_edge((x - 1, y), (x, y), weight = 1.0)
                    if y > 0:
                        my_map.add_edge((x, y - 1), (x, y), weight = 1.0) 

            #logging.info("Marking the obstacles in the graph")
            for y, line in enumerate(lines):
                for x, item in enumerate(line[:-1]):
                    if item in ("T", "@"):
                        #print(y,x, item)
                        my_map.remove_node((x, y))
                        my_map.add_node((x,  y))
                        my_map.nodes[(x, y)]["obstacle"] = True
                    else:
                        self.free_nodes.append((x,  y ))

        self.map = my_map

        # Optimized A*
        self.G_nk = nk.nxadapter.nx2nk(self.map, weightAttr='weight')
        self.nk_node_id = dict((id, u) for (id, u) in zip(self.map.nodes(), range(self.map.number_of_nodes())))
        self.nk_reverse_node_id = dict((u, id) for (id, u) in zip(self.map.nodes(), range(self.map.number_of_nodes())))
        self.nk_heuristic = [0 for _ in range(self.G_nk.upperNodeIdBound())]
    
    def reset(self):
        """
        Resets the environment back to the original state with no agents
        """
        self.generate_map(self.current_map_file)
    
    def update_agent_on_map(self, agent, pos_prev, pos_next):
        if pos_prev != pos_next: # BECAUSE A* RETURNS THE START POSITION, REMEMBER TO CHANGE ASSERT LATER
            
            self.map.nodes[pos_next]["agent"] = agent
            if self.map.nodes[pos_prev]["agent"] is agent:
                self.map.nodes[pos_prev]["agent"] = None
        else:
            self.map.nodes[pos_next]["agent"] = agent


