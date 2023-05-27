# Library imports

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import random
import copy
import math

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Map.map import Map #
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent


class Herd_agent(Agent):
    def __init__(self, map: Map, panic_time_limit: int = 7, repetition_threshold: int = 5, waiting_threshold: int = 3):
        super().__init__(map)
        # Action Related Variables
        self.turn_executed: str = "no" # can be "no", "processing" or "yes"
        self.action: str = "wait"
        self.step: int = 0
        self.neighboring_agents = []
        self.path_history = []
        # Herd Related Varibales
        self.threat_epicenter = None
        self.panic_mode: bool = False
        self.panic_time: int = 0 # timestep of end of panic episode
        self.panic_time_limit: int = panic_time_limit
        # Deadlock/Livelock Related Variables
        self.repetition_threshold: int = repetition_threshold
        self.waiting_time: int = 0
        self.waiting_threshold: int = waiting_threshold

    def find_neighbors(self, depth):
        # Finds the positions of the neighbors excluding the agents' own position
        neighbors = set([self.position])
        for _ in range(depth):
            for n in neighbors.copy():
                neighbors.update(self.map.map.neighbors(n))
        neighbors.remove(self.position)
        return neighbors
    
    def find_neighboring_agents(self):
        # Find agents (agent objects, NOT positions!!!)
        neighbors_list = self.find_neighbors(2)
        agents = []
        # Only save those neighbors that have an Agent placed on them
        for x in neighbors_list:
            if self.map.map.nodes.get(x, {}).get("agent") is not None:  # Check if the node has an agent placed on it
                agents.append(self.map.map.nodes.get(x, {}).get("agent"))
        self.neighboring_agents = agents

    def move(self, step):
        self.step = step
        # TODO: Make swarm call move on the agents in a random order to avoid some agents being preferred.

        self.turn_executed = "processing"
        # Find neighboring agents
        
        # If a panic_mode is finished, reset it to False
        if (self.panic_mode == True) and (self.step == self.panic_time):
            self.replan()
            self.panic_mode = False
            # TODO: Reset other parameters

        # Check if agent is already in panic mode AND if it should still be panicking (if self.step is less than self.panic_time)
        if (self.panic_mode == True) and (self.step < self.panic_time):
            # Move according to herd behavior
            self.step_agent("panic")
        # Check if the herd is panicking aka if a neighboring agent is in panic mode
            # Calculate "this" agents' panic_time and panic movement pattern based on the neighboring agents' panic state
        elif (self.check_herd_panic()): # If True, then this function sets EPICENTER AND OTHER HERD PARAMETERS
            # Move according to herd behavior
            self.step_agent("panic")
        else:
            self.step_agent("regular")

        # MOVE THE AGENT USING THE ORIGINAL AGENT CLASS
        #   Move the agent NOW!

        self.turn_executed = "yes"
        # RESET self.turn_executed back to False
        # Reset all the other shit

    def step_agent(self, move_type):
            # TODO: You should not check agents' next nodes if they are in panic state!, then you are avoiding a collision that will not happen
            # TODO: Update agent self_waiting time after each move
            # NOTE: Swarm has to check if agent.turn_executed is True, because if someone else called it, then it has to "continue" in the loop
            # NOTE: After swarm has called move_all_agents, it has to reset their turn_executed variables
            # NOTE: Swarm should keep track of the step variable
            # TODO: When checking for conflicts (and other places probably), you cannot look at the agents who already has moved, they are a STEP AHEAD and should not go into the calculation the same way, in that case just "wait"
        if move_type == "panic":
            possible_escape_nodes = self.get_escape_nodes()
            if len(possible_escape_nodes) == 0:
                self.action = "wait"
                return
            else:
                # Pick a random agent position, if the chosen one is located on an agent then call move on it
                while len(possible_escape_nodes) != 0:
                    idx = random.randint(0, len(possible_escape_nodes)-1)
                    possible_escape_node = possible_escape_nodes[idx]
                    # Check if there is an agent present on that node and if there is, attempt to move it


                    possible_escape_nodes.pop(idx)  # Pop the element from the list

        
            pass
        elif move_type == "regular":
            # First check for deadlocks or livelocks, if they are present they should be dealt with first!
            if self.deadlock_livelock_detection():
                self.threat_epicenter = self.position
                self.panic_time = self.step + self.panic_time_limit    # Set self.panic_time (set it to a constant hyperparameter defined in the init for now)
            # If no deadlocks or livelocks present we need to check for collisions
            else:
                if self.check_opposite_conflict(): # Check self.path[0] aka (t+1) for opposite conflict
                    neighbor = self.get_agent_by_tag(self.path[0])
                    priority_agent = self.calculate_priority()
                    priority_neighbor = neighbor.calculate_priority()
                    if priority_agent >= priority_neighbor: # TODO: This is a problem, because if we call move on the other agent and it determines that it has priority, they will both end up in the else statement and wait forever
                        if neighbor.turn_executed == "no":
                            neighbor.move()
                            if neighbor.position == self.path[0]:   # Agent did not succeed in moving -> Must mean it is stuck
                                neighbor.turn_executed = "no"   # Give the neighbor its turn back
                                self.give_way() # Give way because there is nothing else to do
                            else:   # Neighbor did succeed in moving'
                                self.move_forward_safely()
                        else:
                            self.action = "wait"
                    else:
                        self.give_way()
                elif self.check_intersection_conflict():
                    if self.self_has_intersection_priority():
                        self.move_forward_safely()
                    else:
                        self.action = "wait"
                else:
                    # Check if there is an agent on the t+1 node
                    # If there is, test if its turn_executed = "no"
                    #   If "no" then, call move() on that agent
                    #   If agent ended up moving
                    #       Call self.move_forward_safely()
                    # else:
                    #   Give that agent its turn back by setting turn_executed = "no"
                    pass
        else:
            print("Error: Illegal Move Type")

    def move_forward_safely(self):
        # Move the agent into its next element in its path (t+1)
        self.action = "move"
        # Assert that there is not an agent in the t+1 node and print "should not happen" so i can see if something went wrong

        if self.is_agent_present_on_node_tag(self.path[0]):
            self.action = "wait"
            print("Error: Agent should not be present on node at this point")
            return False

        if len(self.path) == 0:
            self.map.update_agent_on_map(self, self.target, self.target)
            return False
        
        pos_prev = self.position
        pos_next = self.path.pop(0)

        # update agent position on the map
        self.map.update_agent_on_map(self, pos_prev, pos_next)
        self.position = pos_next

    def give_way(self):
        # TODO: Remember to update the path with more nodes so you can get back
        # TODO: Pick one right or left before picking the one behind you
        pass    
            
    def check_opposite_conflict(self):
        # Is there an agent on the position we want to move into aka next element in our path?
        if self.is_agent_present_on_node_tag(self.path[0]):
            neighbor = self.get_agent_by_tag(self.path[0])
            if (self.path[0] == neighbor.position) and (self.position == neighbor.path[0]):
                return True
        return False
    
    def check_intersection_conflict(self):
        # Intersection is if any neighbor has its t+1 cell the same as our t+1 cell
        self.find_neighboring_agents()
        for neighbor in self.neighboring_agents:
            if (self.path[0] == neighbor.path[0]):
                return True
        return False

    
    def self_has_intersection_priority(self):
        self.find_neighboring_agents()
        neighbors_in_intersection = []
        for neighbor in self.neighboring_agents:
            if (self.path[0] == neighbor.path[0]):
                neighbors_in_intersection.append(neighbor)
        for competing_neighbor in neighbors_in_intersection:
            if competing_neighbor.calculate_priority() > self.calculate_priority():
                return False
        return True


    def is_agent_present_on_node_tag(self, node_tag):
        # Check if there is an agent on the given node tag
        if self.map.map.nodes.get(node_tag, {}).get("agent") is not None:
            return True
        else:
            return False

    def get_agent_by_tag(self, node_tag):
        # Returns the agent object by providing a tag
        return self.map.map.nodes.get(node_tag, {}).get("agent")

    def can_agent_be_moved(self, node_tag):
        # Check if there is an agent present on that node
        if self.map.map.nodes.get(node_tag, {}).get("agent") is not None:
            # Check if we can call move on that agent to make it move away
            agent_to_move = self.map.map.nodes.get(node_tag, {}).get("agent")
            if agent_to_move.turn_executed == "no":
                return True # The agent_to_move has not executed its turn yet, so it can be moved
            else:
                return False # The agent is in the process of moving or has already moved, so we can't make it move
        else:
            return True # There is no agent on 

    def check_herd_panic(self):
        for neighbor in self.neighboring_agents:    # Check all neighboring agents
            if neighbor.panic_mode == True:         # If one is panicking (pick the first one that is)
                neighbor_panic_time = neighbor.panic_time - 2
                if (self.step >= neighbor_panic_time):   # If the herd panic is ending (step is bigger than panic time), return false
                    return False
                self.threat_epicenter = neighbor.threat_epicenter   # Copy its threat_epicenter
                self.panic_mode = True
                self.panic_time = neighbor_panic_time
                return True
        return False

    def calculate_priority(self):
        return len(self.path) # Right now just returning the length of the remaining path, so the agent with longest left to go is given priority
                # Priority based on x*time_alive + y*path_length + z*remaining_path_length + ... (Hyperparameters traned by GA for each map type)
                #    - Agent with lowest priority finds free neighboring node and give way however

    def deadlock_livelock_detection(self):
        # Is the agent at the same position for x time.
        if self.waiting_time > self.waiting_threshold:
            return True
        # Is the agent fucking around location(s) 
        if self.check_repetition():
            return True
        return False

    def replan(self):
        """
        Replan the path to the target from the agent position
        """
        self.path = nx.astar_path(self.map.map, self.position, self.target)
    
    def check_repetition(self):
        if len(self.path_history) >= (len(set(self.path_history)) + self.repetition_threshold):
            return True # There are repeated elements in the list
        return False

    def is_node_safe(self, node_tag):
        # check if node contains agent
        # if self.map.map.nodes.get(node_tag, {}).get("agent") is not None:
        #     return False
        if math.hypot(self.position[0] - self.threat_epicenter[0] , self.position[1] - self.threat_epicenter[1]) > math.hypot(node_tag[0] - self.threat_epicenter[0] , node_tag[1] - self.threat_epicenter[1]):
            return False
        else:
            return True 
        
    def get_escape_nodes(self):
        neighbors = []
        for neighbor in self.find_neighbors(1):
            if self.is_node_safe(neighbor):
                neighbors.append(neighbor)
        return neighbors
        

        """
I flokadfærdskal du tjekke på om der er nogen der skal ind i den celle du har valgt i t+1
	- Hvis der er nogen, skal du vælge en anden celle
	- Hvis den celle du vælger har en robot skal du move den, hvis den er ledig bagefter og 
		ingen andre robotter har den som t+1 (dette skal tjekkes efter naboen har lavet move() og ikke før pga den også kan gå i panic og ændre rute) i sin path, så vælg den
		ellers
			søg videre

Normalt adfærd
	Tjek t+1 celle
		Er det opposite conflict?
			Hvis ja, så tjek prioritet
				Har jeg prioritet, så kald move() på den anden (tjek ofc om den allerede har movet)
					Er den stadig ikke bevæget sig efter må det betyde den er stuck!
						Så må jeg give_way() selvom jeg har prioritet
						Giv den agent vi kaldte move() på sin tur tilbage, da den ikke
							fik flyttet sig
        """