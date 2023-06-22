# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
from typing import List
import time

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent
from Swarm.swarm import Swarm
from Renderer.renderer import Renderer

START_POSITION = 0
TARGET_POSITION = 1

class Simulator:
    """ The Simulator"""

    def __init__(self, map: Map, swarm: Swarm, renderer: Renderer, display: bool = True, max_timestep: int = 100, positions_for_agents = []):
        """ Create the simulator
        :my_map: The map generated for the simulation
        :display: If True, the simulation is displayed visually
        """
        self.map = map
        self.swarm = swarm
        self.renderer = renderer
        self.display = display
        self.max_timestep = max_timestep
        self.step = 0
        self.positions = positions_for_agents
        self.solved = None
        self.makespan = 0
        self.simulation_time = 0
        
    def reset(self):
        self.step = 0
        self.makespan = 0
        self.simulation_time = 0
        for agent in self.swarm.agents:
            agent.step = 0
            agent.steps_moved = 0 
            # self.map.map.nodes[agent.position]["agent"] = None
            # self.map.map.nodes[agent.target]["target"] = None

    def stop(self) -> bool:
        # Stop the simulation
        # returns: If stop criteria is reached
        if self.step > self.max_timestep:
            self.solved = False
            return True
        else:
            return False
        #return self.step > self.max_timestep

    def generate_new_start_target_positions(self):
        self.swarm.set_initial_start_positions_of_agents()
        self.swarm.set_initial_target_positions_of_agents()
        return [self.swarm.start, self.swarm.target]

    def main_loop(self):

        self.reset()
        if len(self.positions) != 0:
            self.swarm.set_initial_start_positions_of_agents(start_positions=self.positions[START_POSITION])
            self.swarm.set_initial_target_positions_of_agents(target_positions=self.positions[TARGET_POSITION])
        elif len(self.swarm.start) > 0:
            self.swarm.set_initial_start_positions_of_agents(start_positions=self.swarm.start)
            self.swarm.set_initial_target_positions_of_agents(target_positions=self.swarm.start)
        else:
            self.generate_new_start_target_positions()
        
        self.swarm.calculate_all_agent_paths()
        
        #TODO REMOVE
        #self.swarm.print_pos()
        start_time = time.perf_counter()
        while not self.stop():
            if self.display:
                self.renderer.display_frame(self.step)
            if self.swarm.move_all_agents(self.step):
                self.makespan = self.step
                self.solved = True 
                if self.display:
                    for i in range(10):   
                        self.renderer.display_frame(self.step)
                        self.step += 1
                #print("Finished Early in ", self.step, " steps")
                break
            elif self.swarm.all_agents_reached_target_once():
                self.solved = True
                self.makespan = self.step
                if self.display:
                    for i in range(10):   
                        self.renderer.display_frame(self.step)
                        self.step += 1
                break
            self.step += 1
        end_time = time.perf_counter()
        self.simulation_time = end_time - start_time
        if self.makespan == 0:
            self.makespan = self.step - 1
            self.solved = False
        # Calculate sum of costs
        cost = 0
        for agent in self.swarm.agents:
            cost += agent.steps_moved
        #print(f"waits: {sum(self.swarm.waitcount_trafic)} conflicts: {sum(self.swarm.conflictcount)}")
        return cost, self.makespan

    def numpy_to_list_of_tuple(self, list):
        if len(list) > 0:                            # Any element in list
            list_of_tuple = list.tolist()
            for idx1, both_position in enumerate(list_of_tuple):      #start and target
                for idx2, position in enumerate(both_position):
                    list_of_tuple[idx1][idx2] = tuple(position)
            return list_of_tuple

    


