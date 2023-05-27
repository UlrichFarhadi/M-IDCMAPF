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
import math
import cv2
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
                rule_order=[0,1,2,3,4,5,6],
                save_trainings_animation = False) -> None:
        super().__init__(num_best_solutions_to_save, population_size, mutation_rate, elitism, max_num_generations)
        self.fitness_exponent = 3
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
        #self.training_frames=[]
        self.save_trainings_animation = save_trainings_animation
    
    # Define the problem-specific fitness function
    def fitness(self, chromosome, start_position, target_position):
        #cost = 0
        cost = []
        if self.inter:
            chromosome = np.array(chromosome).reshape(self.inter_anchorpoints_width,self.inter_anchorpoints_height).tolist()
        for i in range(self.num_env_repetitions):
            cost_tmp, span = delayed(self.environment_function, nout=2)(chromosome,
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
                                            max_timestep = self.max_timestep,
                                            rule_order = self.rule_order)
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

    def generate_initial_population(self):
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


    def run(self):
        # cluster = LocalCluster()
        # client = Client(cluster)
        # print(f"Link to dask dashboard {client.dashboard_link}")

        # Write in a terminal. dask scheduler
        # Write in another terminal: dask worker <ip from scheduler (connect worker at.. that ip)>
        # Connect another pc using the same as previous step, the reason we also need a worker on the main pc is so that it is also a worker!
        #client = Client("10.126.85.122:8786")


        def sort_by_second_element(item):
            return item[1]
        
        if self.inter:
            population = self.generate_initial_population_interpolation()
        else:
            population = self.generate_initial_population()

        for gen in tqdm(range(self.max_num_generations), desc="Genetic Algorithm Processing...", leave=False):
            #generate_new_start_target_positions()
            if len(self.start_positions) == 0 and len(self.target_positions) == 0:
                start_position, target_position = self.generate_new_start_target_positions()
            else:
                start_position, target_position = self.start_positions,self.target_positions
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
                if self.save_trainings_animation:
                    self.plot_directions(self.map.map_width, self.map.map_height, self.map.free_nodes, self.list_of_best_solutions[0][0],gen,self.env)
                    # self.create_animation()
                #print("\nBest Solution gen: ", gen, " is ", self.list_of_best_solutions[0])
                print("\nBest Solution gen: ", gen)
                sum_of_costs = (1000000 / self.list_of_best_solutions[0][1]) ** (1. / self.fitness_exponent)
                print("Best Sum of Costs: ", sum_of_costs)

            if gen%1 == 0:
                self.write_to_csv(self.list_of_best_solutions[0][0], sum_of_costs, os.path.basename(self.env) + "_" + str(self.amount_of_agents) + ".csv")
                # print(self.list_of_best_solutions[0])
                
            self.best_sumofcosts = 999999999

            if len(self.start_positions) == 0 and len(self.target_positions) == 0:
                start_position, target_position = self.generate_new_start_target_positions()
            else:
                start_position, target_position = self.start_positions,self.target_positions
            

        
        
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
        
    def write_to_csv(self, weight_list, sum_of_costs, filename='output.csv', append=True):
        # If append is True, open the CSV file in append mode
        mode = 'a' if append else 'w'
        
        # Open the CSV file in the specified mode
        with open(filename, mode, newline='') as file:
            writer = csv.writer(file)
            
            # If append is False, write the header row
            if not append:
                writer.writerow(['weight_list', 'sum_of_costs'])
            
            # Loop through the elements of the two lists
            #for i in range(len(int(sum_of_costs))):
                # Get the corresponding elements from the lists
                #soc = sum_of_costs[i]
                
                
                # Append the experiment list (as a string) to the CSV file
            writer.writerow([weight_list, sum_of_costs])




    def plot_directions(self, map_width, map_height, coordinates, angles, gen, env):
        plt.clf()
        fig = plt.gcf()
        ax = plt.gca()
        #fig, ax = plt.subplots()

        # Plot the coordinates
        for x, y in coordinates:
            ax.plot(x, y)

        # Add arrows for each angle
        for i, angle in enumerate(angles):
            if i % 2 == 0:
                x, y = coordinates[int(i/2)]
                x += 0.5
                y += 0.5
                scale = 0.5
                ax.annotate("", xy=(x + scale*math.cos(math.radians(angle*360)), y + scale*math.sin(math.radians(angle*360))), xytext=(x, y),
                            arrowprops=dict(arrowstyle="->", color='black'), annotation_clip=False)

        plt.xlim(0,map_width)
        plt.ylim(0,map_height)
        ax.set_xticks(range(0, map_width+1))
        ax.set_yticks(range(0, map_height+1))
        ax.set_aspect('equal')
        plt.grid(True,'both',"both")
        plt.title(f" Map: {os.path.splitext(os.path.basename(env))[0]} \n Generation: {gen}")
        plt.draw()
        plt.show(block=False)
        plt.pause(0.0000001)

        plt.savefig("temp_frames/tmp_frame_"+str(len(os.listdir("temp_frames")))+".png", dpi=400)
        #plt.savefig("tmp_frame.png", dpi=self.dpi)
        #frame = cv2.imread("tmp_frame.png")
        #self.training_frames.append(frame)


    def create_animation(self, filename='test_animation.mp4', fps=1):
        if len(os.listdir("temp_frames")) == 0:
            print("No frames found in temp_frames")
        else:
            # Get the height and width of the first image
            img = cv2.imread("temp_frames/tmp_frame_0.png")
            height, width, layers = img.shape

            # Create the video writer object
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(filename, fourcc, fps, (width,height))

            # Iterate through each image and add it to the video
            for i in range(len(os.listdir("temp_frames"))):
                png = cv2.imread("temp_frames/tmp_frame_"+str(i)+".png")
                video_frame = cv2.cvtColor(png, cv2.COLOR_RGBA2RGB)
                video.write(video_frame)

            # Release the video writer
            video.release()

            for i in os.listdir("temp_frames"):
                os.remove("temp_frames/"+i)

    # def create_animation(self, filename='test_animation.mp4', fps=1):
    #     # Get the height and width of the first image
    #     img = self.training_frames[0]
    #     height, width, layers = img.shape

    #     # Create the video writer object
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     video = cv2.VideoWriter(filename, fourcc, fps, (width,height))

    #     # Iterate through each image and add it to the video
    #     for png in self.training_frames:
    #         video_frame = cv2.cvtColor(png, cv2.COLOR_RGBA2RGB)
    #         video.write(video_frame)

    #     # Release the video writer
    #     video.release()


# plot_directions(10, 10, [(1,2),(2,3),(3,4)], [0, 20, 30])
# plot_directions(10, 10, [(1,2),(2,3),(3,4)], [0, 40, 46])
# plot_directions(10, 10, [(1,2),(2,3),(3,4)], [0, 50, 270])
# plot_directions(10, 10, [(1,2),(2,3),(3,4)], [0, 60, 80])
# plot_directions(10, 10, [(1,2),(2,3),(3,4)], [0, 23, 55])
