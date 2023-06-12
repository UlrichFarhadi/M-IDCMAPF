# Library imports
import sys
import os
import copy
import random
import numpy as np
from typing import List, Tuple, Callable
from tqdm import tqdm
from dask.distributed import Client, LocalCluster
from dask import delayed
from dask import compute
import time
import csv
from scipy.interpolate import interp2d
from statistics import mean

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir) 

from GA.GA_template import GA_template
from Simulator.simulator import Simulator
from IDCMAPF_Tests.tests import *

class GA_Fluid(GA_template):
    def __init__(self,
                environment_function,
                env,
                start_positions = None,
                target_positions = None,
                num_best_solutions_to_save: int = 10,
                population_size: int = 20,
                mutation_rate: float = 0.1,
                elitism: int = 3,
                max_num_generations: int = 500,
                inter: bool = False,
                inter_anchorpoints_width: int = 8,
                inter_anchorpoints_height: int = 8,
                edge_weight_encoding: bool = True,
                budget: int = 20000,

                amount_of_agents = 10,
                mutation_rate_swap = 0.05,
                mutation_rate_point = 0.10,
                agent_type=IDCMAPF_agent,
                delay=0.0001,
                fig_size_factor=20,
                node_size=10,
                linewidth=0.5,
                dpi=40,
                display=False,
                max_timestep=1000,
                rule_order=[0,1,2,3,4,5,6]) -> None:
        super().__init__(num_best_solutions_to_save, population_size, mutation_rate, elitism, max_num_generations)
        self.fitness_exponent = 9
        self.num_env_repetitions = 5
        self.environment_function = environment_function
        self.rule_order=rule_order
        self.best_sumofcosts = 999999999
        self.map = Map_directed()
        self.map.generate_map(env)
        self.env = env
        self.start_positions = start_positions
        self.target_positions = target_positions
        self.inter = inter
        self.inter_anchorpoints_width = inter_anchorpoints_width
        self.inter_anchorpoints_height = inter_anchorpoints_height
        self.edge_weight_encoding = edge_weight_encoding
        self.config_max_gen = int(budget / (self.population_size * self.num_env_repetitions))

        self.mutation_rate_swap = mutation_rate_swap
        self.mutation_rate_point = mutation_rate_point
        self.amount_of_agents = amount_of_agents
        self.agent_type = agent_type
        self.delay = delay
        self.fig_size_factor = fig_size_factor
        self.node_size = node_size
        self.linewidth = linewidth
        self.dpi = dpi
        self.display = display
        self.max_timestep = max_timestep


        self.moving_window = []
        self.moving_window_size = 10
        self.moving_window_threshold = 5
        self.last_moving_avg = 9999999999999
        self.bad_moving_counter = 0

    
    # Define the problem-specific fitness function
    def fitness(self, chromosome, start_position, target_position):
        #cost = 0
        cost = []
        if self.inter:
            chromosome = np.array(chromosome).reshape(self.inter_anchorpoints_width,self.inter_anchorpoints_height).tolist()
        for i in range(self.num_env_repetitions):
            cost_tmp, span = delayed(self.environment_function, nout=2)(chromosome,
                                            start_position[i],
                                            target_position[i],
                                            self.env,
                                            amount_of_agents = self.amount_of_agents,
                                            agent_type = self.agent_type,
                                            delay = self.delay,
                                            fig_size_factor = self.fig_size_factor,
                                            node_size = self.node_size,
                                            linewidth = self.linewidth,
                                            dpi = self.dpi,
                                            display = self.display,
                                            max_timestep = self.max_timestep,
                                            rule_order = self.rule_order,
                                            edge_weight_encoding = self.edge_weight_encoding)
            #cost += cost_tmp
            cost.append(cost_tmp)
        cost = sum(compute(*cost)) / self.num_env_repetitions
        # if cost < self.best_sumofcosts:
        #     self.best_sumofcosts = cost 
        return (cost**self.fitness_exponent)
    # Define the problem-specific fitness function

    # Define the genetic operators
    def crossover(self, parent1, parent2):
        # Point Crossover
        # Assume that both parents are sequences of the same length
        if len(parent1) != len(parent2):
            raise IndexError("the Parrents are not the same length")
        crossover_point = random.randint(0, len(parent1))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child
    
    def single_element_crossover(parent1, parent2, crossover_probability):
        # Single element crossover:
            # EXAMPLE:
            # parent1 = [1, 2, 3, 4, 5]
            # parent2 = [6, 7, 8, 9, 10]
            # # Perform a single element crossover with a probability of 0.5
            # child = single_element_crossover(parent1, parent2, 0.5)
            # print(child)
            # [1, 7, 3, 4, 10]

        if len(parent1) != len(parent2):
            raise IndexError("The parents are not the same length")
        child = []
        for i in range(len(parent1)):
            if random.random() <= crossover_probability:
                child.append(parent2[i])
            else:
                child.append(parent1[i])
        return child

    def mutation_swap(self, chromosome):
        # Swap mutation
        for i in range(len(chromosome)):
            mutate = random.random()
            if mutate < self.mutation_rate_swap:
                idx = random.randint(0, len(chromosome)-1)
                # Swap elements at index i and idx
                chromosome[i], chromosome[idx] = chromosome[idx], chromosome[i]

    def mutation_point(self, chromosome):  
        # Point mutation
        if (self.edge_weight_encoding):
            for i in range(len(chromosome)):
                mutate = random.random()
                if mutate < self.mutation_rate_point:
                    # Mutate that element of the cromosome (aka give it a new random value between 0 and 1)
                    mu, sigma = chromosome[i], 0.1666
                    new_weight = np.random.normal(mu, sigma)
                    if new_weight > 1:
                        new_weight = 1                   
                    elif new_weight < 0:
                        new_weight = 0
                    chromosome[i] = new_weight
                    #chromosome[i] += random.random()
        else:
            for i in range(len(chromosome)):
                mutate = random.random()
                if mutate < self.mutation_rate_point:
                    if ((i % 2) == 0):
                        # Mutate that element of the cromosome (aka give it a new random value between 0 and 1)
                        mu, sigma = chromosome[i], 0.1666
                        new_weight = np.random.normal(mu, sigma)
                        if new_weight > 1:
                            new_weight -= 1                   
                        elif new_weight < 0:
                            new_weight += 1
                        chromosome[i] = new_weight
                        #chromosome[i] += random.random()


    def generate_initial_population(self):
        if self.edge_weight_encoding:
            initial_nonshuffled_chromosome = []
            for i in range(len(self.map.get_weight_list())):
                initial_nonshuffled_chromosome.append(0.5)
            
            population = []
            for i in range(self.population_size):
                chromosome_copy = copy.deepcopy(initial_nonshuffled_chromosome)
                population.append([chromosome_copy, 0.0]) # Append the scores
            return population
        else:
            initial_nonshuffled_chromosome = []
            for i in range(len(self.map.free_nodes)):
                initial_nonshuffled_chromosome.append(random.uniform(0, 1)) # Append Vector Angle
                initial_nonshuffled_chromosome.append(random.uniform(0, 1)) # Append Vector Magnitude
            
            population = []
            for i in range(self.population_size):
                chromosome_copy = copy.deepcopy(initial_nonshuffled_chromosome)
                population.append([chromosome_copy, 0.0]) # Append the scores
            return population


        # # Shuffle the chromosome
        # population = []
        # for i in range(self.population_size):  # Append additional shuffled chromosomes
        #     shuffled_chromosome = initial_nonshuffled_chromosome.copy()
        #     random.shuffle(shuffled_chromosome)
        #     population.append([shuffled_chromosome, 0.0]) # [chromosome, initial_predefined_fitness(to be overritten)]
        # return population

    def generate_initial_population_interpolation(self):
        initial_nonshuffled_chromosome = []
        for i in range(self.inter_anchorpoints_width * self.inter_anchorpoints_height):
            initial_nonshuffled_chromosome.append(0.5)
        
        population = []
        for i in range(self.population_size):
            chromosome_copy = copy.deepcopy(initial_nonshuffled_chromosome)
            population.append([chromosome_copy, 0.0]) # Append the scores
        return population

    def roulette_wheel_selection(self, population):
        fitness_scores = [individual[1] for individual in population] # population[:][1]
        total_fitness = sum(fitness_scores)
        selection_probs = [score / total_fitness for score in fitness_scores]
        r = random.uniform(0, 1)
        cumulative_prob = 0
        for i in range(len(selection_probs)):
            cumulative_prob += selection_probs[i]
            if cumulative_prob > r:
                return copy.deepcopy(population[i][0])
    
    def generate_new_population(self, population):
        # population = [[chromosome1, fitness1], [chromosome2, fitness2]....]
        new_population = []
        for i in range(self.population_size):
            #parent1 = self.roulette_wheel_selection(population)
            #parent2 = self.roulette_wheel_selection(population)
            #child = self.crossover(parent1, parent2)   # Cannot crossover in a sequence of unique items
            child = self.roulette_wheel_selection(population)
            self.mutation_swap(child)
            self.mutation_point(child)
            new_population.append([child, 0.0]) # [chromosome, cleared fitness score]

        for elite in range(self.elitism):   # If elitism is a number higher than 0
            new_population[elite] = self.list_of_best_solutions[elite]

        return new_population

    def validator(self, num_agents, env_name, fluid, start_pos, target_pos, rule_order=[0,1,2,3,4,5,6] , display=False):
        def run_one_sim(idx):
            # Create the map object
            map = Map_directed()
            # Import the environment
            env = "Environments/" + env_name + ".map"
            map.generate_map(env)
            map.update_weight_on_map(fluid)
            # Create the swarm object
            swarm = Swarm_IDCMAPF(map, amount_of_agents=num_agents, agent_type=IDCMAPF_agent, rule_order=rule_order)

            # Create the renderer object
            renderer = Renderer(map, delay=0.0001, fig_size_factor=6, node_size=350, linewidth=0.5, dpi=400)
            simulator = Simulator(map, swarm, renderer, display=display, max_timestep=1000, positions_for_agents=[start_pos[idx], target_pos[idx]])
            cost, makespan = simulator.main_loop()
            return cost, makespan        
        
        list_of_cost = []
        list_of_makespan = []
        for idx in range(len(start_pos)):
            # Create the simulator object
            cost, span = delayed(run_one_sim, nout=2)(idx)
            list_of_cost.append(cost)
            list_of_makespan.append(span)

        res = compute(*list_of_cost, *list_of_makespan)
        # if save_video:    
        #     renderer.create_animation("Testvideos/" + env_name + "_" + str(num_agents) + ".mp4", fps=5)
        return sum(res[:len(start_pos)])/len(start_pos), sum(res[len(start_pos):])/len(start_pos)


    def run(self, v_num_agents, v_env_name, v_start_pos, v_target_pos, v_rule_order, csv_filename = "Fluid_chromosome1", start = None, target = None):
        # cluster = LocalCluster()
        # #client = Client(cluster)
        # client = Client("127.0.0.1:8786")
        # print(f"Link to dask dashboard {client.dashboard_link}")

        # Write in a terminal. dask scheduler
        # Write in another terminal: dask worker <ip from scheduler (connect worker at.. that ip)>
        # Connect another pc using the same as previous step, the reason we also need a worker on the main pc is so that it is also a worker!
        #client = Client("127.0.0.1:8786")


        def sort_by_second_element(item):
            return item[1]
        
        if self.inter:
            population = self.generate_initial_population_interpolation()
        else:
            population = self.generate_initial_population()

        #for gen in tqdm(range(self.max_num_generations), desc="Genetic Algorithm Processing...", leave=False):
        gen = -1
        while True:
            gen += 1
            #for gen in tqdm(range(self.max_num_generations)):
            #generate_new_start_target_positions()
            if start is None:
                # if len(self.start_positions) == 0 and len(self.target_positions) == 0:
                start_position, target_position = self.generate_new_start_target_positions(self.num_env_repetitions)
                # else:
                    # start_position, target_position = self.start_positions,self.target_positions
            else:
                start_position, target_position = start[gen], target[gen]
            # Compute the fitness for each chromosome in the population   
            list_of_cost = []
            #list_of_makespan = []
            for idx, (chromosome, _) in enumerate(population):
                #population[idx][1] = self.fitness(chromosome, start_position, target_position)
                cost = delayed(self.fitness, nout=1)(chromosome, start_position, target_position)  
                list_of_cost.append(cost)
                #list_of_makespan.append(makespan)          

            res = compute(*list_of_cost)
            #res = compute(*list_of_cost, *list_of_makespan)
            #res[:population], res[population:]
            for idx in range(len(population)):
                population[idx][1] = 1000000 / res[idx] # Set the score of each chromosome computed with dask before
    
        
            # Use a lambda sort function Append the self.num_best_solutions_to_save of the chromosomes in the self.list_of_best_solutions array
            self.list_of_best_solutions = sorted(population, key=sort_by_second_element, reverse=True)[:self.num_best_solutions_to_save]
            population = self.generate_new_population(population)

            if gen%1 == 0:    # Print some update information
                #print("\nBest Solution gen: ", gen, " is ", self.list_of_best_solutions[0])
                #print("\nBest Solution gen: ", gen)
                sum_of_costs = (1000000 / self.list_of_best_solutions[0][1]) ** (1. / self.fitness_exponent)
                
                mean_sum_of_cost = mean([(1000000 / elem[1]) ** (1. / self.fitness_exponent) for elem in self.list_of_best_solutions])

                worst_sum_of_cost = (1000000 / self.list_of_best_solutions[-1][1]) ** (1. / self.fitness_exponent)

                #print("Best Sum of Costs: ", sum_of_costs)
                self.write_to_csv([sum_of_costs, mean_sum_of_cost, worst_sum_of_cost], csv_filename + ".csv")

            if (gen % (self.config_max_gen - 1)) == 0 and gen != 0:
                # Validate
                v_soc , v_span = self.validator(num_agents=v_num_agents, env_name=v_env_name, fluid=self.list_of_best_solutions[0][0], start_pos=v_start_pos, target_pos=v_target_pos, rule_order=v_rule_order)
                if self.edge_weight_encoding:
                    folder = "edge_weight"
                else:
                    folder = "node_vector" 
                self.write_to_csv([self.population_size, self.mutation_rate_point, self.num_env_repetitions, v_soc, v_span, self.list_of_best_solutions[0][0]], f"Tuning_data_ga/{folder}/validator_test.csv")
                return self.list_of_best_solutions[0][0]
            # if gen%5 == 0:
            #     pass
                # print(self.list_of_best_solutions[0])   
            self.best_sumofcosts = 999999999

            # if len(self.start_positions) == 0 and len(self.target_positions) == 0:
            #     start_position, target_position = self.generate_new_start_target_positions()
            # else:
            #     start_position, target_position = self.start_positions,self.target_positions
            

            # # Moving Window 
            # if len(self.moving_window) < self.moving_window_size:
            #     self.moving_window.append(sum_of_costs)
            # else:
            #     self.moving_window.append(sum_of_costs)
            #     if len(self.moving_window) > self.moving_window_size:
            #         self.moving_window.pop(0)
            #     avg = sum(self.moving_window)/self.moving_window_size
            #     if avg < self.last_moving_avg:
            #         self.last_moving_avg = avg
            #         self.bad_moving_counter = 0
            #     else:
            #         self.bad_moving_counter += 1
            #         if self.bad_moving_counter >= self.moving_window_threshold:
            #             return self.previous_chromosome
            # self.previous_chromosome = self.list_of_best_solutions[0][0]

                 
            

        
        
    def generate_new_start_target_positions(self, num_rep):
        start_pos = []
        target_pos = []
        for _ in range(num_rep):
            start = []
            target = []
            start_positions = copy.deepcopy(self.map.free_nodes)
            for i in range(self.amount_of_agents):
                node_tag = random.choice(start_positions)
                start_positions.remove(node_tag)
                start.append(node_tag)

            target_positions = copy.deepcopy(self.map.free_nodes)
            for i in range(self.amount_of_agents):
                node_tag = random.choice(target_positions)
                target_positions.remove(node_tag)
                target.append(node_tag)
            start_pos.append(start)
            target_pos.append(target)
        return start_pos, target_pos
        
    def write_to_csv(self, info, filename='output.csv', append=True):
        # If append is True, open the CSV file in append mode
        mode = 'a' if append else 'w'
        
        # Open the CSV file in the specified mode
        with open(filename, mode, newline='') as file:
            writer = csv.writer(file)
            

            writer.writerow(info)