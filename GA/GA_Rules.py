# Library imports
import sys
import os
import copy
import random
import numpy as np
from typing import List, Tuple, Callable
from tqdm import tqdm
# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir) 

from GA.GA_template import GA_template
from Simulator.simulator import Simulator
from IDCMAPF_Tests.tests import *

class GA_Priority_rules(GA_template):
    def __init__(self,
                environment_function,
                env,
                num_best_solutions_to_save: int = 10,
                population_size: int = 20,
                mutation_rate: float = 0.1,
                elitism: int = 3,
                max_num_generations: int = 500,

                amount_of_agents = 10,
                agent_type=IDCMAPF_agent,
                delay=0.0001,
                fig_size_factor=20,
                node_size=10,
                linewidth=0.5,
                dpi=40,
                display=False,
                max_timestep=1000) -> None:
        super().__init__(num_best_solutions_to_save, population_size, mutation_rate, elitism, max_num_generations)
        self.fitness_exponent = 1
        self.environment_function = environment_function
        self.number_of_rules = 7
        self.best_sumofcosts = 999999999
        self.map = Map()
        self.map.generate_map(env)
        self.env = env

        self.amount_of_agents = amount_of_agents
        self.agent_type = agent_type
        self.delay = delay
        self.fig_size_factor = fig_size_factor
        self.node_size = node_size
        self.linewidth = linewidth
        self.dpi = dpi
        self.display = display
        self.max_timestep = max_timestep


    # Define the problem-specific fitness function
    def fitness(self, chromosome, start_position, target_position):
        cost = 0
        num_env_repetitions = 5
        for i in range(num_env_repetitions):
            cost += self.environment_function(chromosome,
                                            start_position,
                                            target_position,
                                            self.env,
                                            amount_of_agents = self.amount_of_agents,
                                            agent_type = self.agent_type,
                                            delay = self.delay,
                                            fig_size_factor = self.fig_size_factor,
                                            node_size = self.node_size,
                                            linewidth = self.linewidth,
                                            dpi = self.dpi,
                                            display = self.display,
                                            max_timestep = self.max_timestep)
        cost = cost / num_env_repetitions
        if cost < self.best_sumofcosts:
            self.best_sumofcosts = cost

        return 10000 / (cost**self.fitness_exponent)

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

    def mutation(self, chromosome):
        # Swap mutation
        for i in range(len(chromosome)):
            mutate = random.random()
            if mutate < self.mutation_rate:
                idx = random.randint(0, len(chromosome)-1)
                # Swap elements at index i and idx
                chromosome[i], chromosome[idx] = chromosome[idx], chromosome[i]

    def generate_initial_population(self):
        initial_nonshuffled_chromosome = []
        for i in range(self.number_of_rules):
            initial_nonshuffled_chromosome.append(i)            

        # Shuffle the chromosome
        population = []
        for i in range(self.population_size):  # Append additional shuffled chromosomes
            shuffled_chromosome = initial_nonshuffled_chromosome.copy()
            random.shuffle(shuffled_chromosome)
            population.append([shuffled_chromosome, 0.0]) # [chromosome, initial_predefined_fitness(to be overritten)]
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
            self.mutation(child)
            new_population.append([child, 0.0]) # [chromosome, cleared fitness score]

        for elite in range(self.elitism):   # If elitism is a number higher than 0
            new_population[elite] = self.list_of_best_solutions[elite]

        return new_population


    def run(self):
        def sort_by_second_element(item):
            return item[1]
        population = self.generate_initial_population()

        #generate_new_start_target_positions()
        start_position, target_position = self.generate_new_start_target_positions()
        for gen in tqdm(range(self.max_num_generations), desc="Genetic Algorithm Processing...", leave=False):
            # Compute the fitness for each chromosome in the population      
            for idx, (chromosome, _) in enumerate(population):
                population[idx][1] = self.fitness(chromosome, start_position, target_position)
            
                
            # Use a lambda sort function Append the self.num_best_solutions_to_save of the chromosomes in the self.list_of_best_solutions array
            self.list_of_best_solutions = sorted(population, key=sort_by_second_element, reverse=True)[:self.num_best_solutions_to_save]
            population = self.generate_new_population(population)

            if gen%1 == 0:    # Print some update information
                print("\nBest Solution gen: ", gen, " is ", self.list_of_best_solutions[0])
                print("Best Sum of Costs: ", self.best_sumofcosts)
            self.best_sumofcosts = 999999999

            start_position, target_position = self.generate_new_start_target_positions()
            

        
        
    def generate_new_start_target_positions(self):
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
        return start, target
        