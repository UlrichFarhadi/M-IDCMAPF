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

from GA_template import GA_template

class GA_travelling_salesman(GA_template):
    def __init__(self, num_best_solutions_to_save: int = 10, population_size: int = 100, mutation_rate: float = 0.1, elitism: int = 3, max_num_generations: int = 100) -> None:
        super().__init__(num_best_solutions_to_save, population_size, mutation_rate, elitism, max_num_generations)
        self.number_of_cities = 10
        self.region_y_limit = [0, 10]
        self.region_x_limit = [0, 10]
        self.cities = []
        self.fitness_exponent = 4

    # Define the problem-specific fitness function
    def fitness(self, chromosome):
        cost = 0
        for i in range(len(chromosome) - 1):
            city1 = self.cities[chromosome[i]]
            city2 = self.cities[chromosome[i+1]]
            distance = np.linalg.norm(np.array(city2) - np.array(city1))
            cost += distance
            # cost = cost ** N # Modify the cost function so it scales exponentially
        return 1/(cost**self.fitness_exponent)

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
        for i in range(self.number_of_cities):
            initial_nonshuffled_chromosome.append(i)            
            self.cities.append([random.uniform(self.region_y_limit[0], self.region_y_limit[1]), random.uniform(self.region_x_limit[0], self.region_x_limit[1])])
        #self.cities = [[0.5, 0.001], [0.6, 0.001], [2.3, 0.001], [3.15, 0.001], [5.02, 0.001], [7.5, 0.001], [7.55, 0.001], [7.8, 0.001], [8.1, 0.001], [9.8, 0.001]]
        self.cities = [[5.02, 0.001], [0.6, 0.001], [9.8, 0.001], [8.1, 0.001], [0.5, 0.001], [7.5, 0.001], [7.55, 0.001], [7.8, 0.001], [3.15, 0.001], [2.3, 0.001]]
        # Best solution is [4, 1, 9, 8, 0, 5, 6, 7, 3, 2]

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

        print("Cities: ", self.cities)

        for gen in tqdm(range(self.max_num_generations), desc="Genetic Algorithm Processing...", leave=False):
            # Compute the fitness for each chromosome in the population      
            for idx, (chromosome, _) in enumerate(population):
                population[idx][1] = self.fitness(chromosome)
            
                
            # Use a lambda sort function Append the self.num_best_solutions_to_save of the chromosomes in the self.list_of_best_solutions array
            self.list_of_best_solutions = sorted(population, key=sort_by_second_element, reverse=True)[:self.num_best_solutions_to_save]
            population = self.generate_new_population(population)

            if gen%1 == 0:    # Print some update information
                print("Best Solution gen: ", gen, " is ", self.list_of_best_solutions[0])
            
        
        
        