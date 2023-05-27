import csv
import os
import sys

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from Simulator.simulator import Simulator


class Logger:
    def __init__(self, sim):
        self.data = []
        self.simulator = sim


    def sum_of_cost(self):
        cost = 0
        for agent in self.simulator.swarm.agents:
            cost += agent.steps_moved
        return cost


    def log(self, map_name = None, map_size = None, obstacles_number = None, num_agents = None, solver = None, solved = None, soc = None, makespan = None, simulation_time = None):
        map_name = self.simulator.map.map_name
        map_size = f"{self.simulator.map.map_width}x{self.simulator.map.map_height}"
        obstacles_number = self.simulator.map.map_width*self.simulator.map.map_height - len(self.simulator.map.free_nodes)
        num_agents = self.simulator.swarm.amount_of_agents
        solver = "Bovl"
        solved = self.simulator.solved
        soc = self.sum_of_cost()
        makespan = self.simulator.makespan
        simulation_time = self.simulator.simulation_time
        self.data.append({
            'map_name': map_name,
            'map_size': map_size,
            'obstacles_number': obstacles_number,
            'num_agents': num_agents,
            'solver': solver,
            'solved': solved,
            'sum of cost': soc,
            'makespan': makespan,
            'simulation_time': simulation_time
        })

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['map_name', 'map_size', 'obstacles_number', 'num_agents', 'solver', 'solved', 'sum of cost', 'makespan', 'simulation_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

