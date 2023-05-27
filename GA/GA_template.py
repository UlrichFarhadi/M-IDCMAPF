# Library imports
import sys
import os
import copy
import random
import numpy
from typing import List, Tuple, Callable

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir) 



class GA_template:
    def __init__(self, num_best_solutions_to_save: int = 10, population_size: int = 100, mutation_rate: float = 0.01, elitism: int = 0, max_num_generations: int = 500) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.max_num_generations = max_num_generations
        self.num_best_solutions_to_save = num_best_solutions_to_save
        self.list_of_best_solutions = [] # [[fitness, chromosome or solution].[]...n]

    
    # Define the problem-specific fitness function
    def fitness(self, chromosome):
        raise NotImplementedError("A fitness function must be provided")

    # Define the genetic operators
    def crossover(self, parent1, parent2):
        # Assume that both parents are sequences of the same length
        if len(parent1) != len(parent2):
            raise IndexError("the Parrents are not the same length")
        crossover_point = random.randint(0, len(parent1))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutation(self, chromosome):
        # Assume that the chromosome is a list of floats
        mutated_chromosome = []
        for gene in chromosome:
            if random.random() < self.mutation_rate:
                # Add or subtract a small random value to the gene
                mutated_gene = gene + random.uniform(-0.1, 0.1)
                mutated_chromosome.append(mutated_gene)
            else:
                mutated_chromosome.append(gene)
        return mutated_chromosome
        
    def generate_initial_population(self):
        # Override this function with a problem specific one
        raise NotImplementedError("A *** function must be provided")

    def selection(self):
        # Override this function with a problem specific one
        raise NotImplementedError("A *** function must be provided")

    def run(self):
        # Override this function with a problem specific one
        raise NotImplementedError("A eval function must be provided")

    
        
    # # Initialize the population
    # population = []
    # for i in range(population_size):
    #     # TODO: Create a random chromosome and add it to the population
    #     pass

    # # Main GA loop
    # for generation in range(num_generations):
    # # Evaluate the fitness of each chromosome in the population
    # fitnesses = [fitness(chromosome) for chromosome in population]
    
    # # Select parents for reproduction
    # parents = []
    # for i in range(2):
    #     # TODO: Implement parent selection, e.g. using tournament selection or roulette wheel selection
    #     pass
    #     parents.append(parent)
    
    # # Create a new population through reproduction
    # new_population = []
    # while len(new_population) < population_size:
    #     child = crossover(parents[0], parents[1])
    #     if random.random() < mutation_rate:
    #         child = mutation(child)
    #     new_population.append(child)
    
    # # Replace the old population with the new population
    # population = new_population
    
    # # Print the best chromosome in the population for this generation
    # best_chromosome = population[fitnesses.index(max(fitnesses))]
    # print(f"Generation {generation}: Best fitness = {fitness(best_chromosome)}")
    
    