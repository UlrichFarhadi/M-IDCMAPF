import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import csv
import ast

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '../..'))
sys.path.append(parent_dir)

dotbool = True
folder_path = "GA_Training_Benchmark_Maps/Traffic"
def load_obstacles(env):
    filename = f"Traffic/obstacles_env/{env}.csv"
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data = ast.literal_eval(row[0])
        return data
    
data = {}
matrix_with_info = []
# List all files in the folder
file_list = [item for item in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, item))]


# Filter and sort the file list based on the 'i' value
file_list = sorted(file_list, key=lambda x: int(x.split("_")[-1].split(".")[0]))

experments_size = 250
current_experiment = []
experments_sums = []

def process_group(matrix_group):
    group_sum = np.sum(matrix_group, axis=0)
    return group_sum

for filename in file_list:
    matrix = np.loadtxt(os.path.join(folder_path, filename))  # Adjust loading based on your matrix format
    current_experiment.append(matrix)
    
    if len(current_experiment) == experments_size:
        experments_sums.append(process_group(current_experiment))
        current_experiment = []


# Process any remaining matrices in the last group
if current_experiment:
    print("ERROR")


print("Sums of each:")
for i, experments_sum in enumerate(experments_sums):
    print(f"experiment {i + 1} sum:\n{experments_sum}")

map_name_csv, num_agents_csv, rule_order_csv, encoding_scheme_csv, mutation_rate_csv, environment_repetitions_csv, pop_size_csv, budget_csv = 0,1,2,3,4,5,6,7
logging_status_filename = "GA_Training_Benchmark_Maps/cases.csv"
with open(logging_status_filename, 'r') as log_file:
    csv_reader = csv.reader(log_file)
    next(csv_reader)
    for matrix,row in zip(experments_sums,csv_reader):
        map_name = row[map_name_csv]
        num_agents = int(row[num_agents_csv])
        rule_order = ast.literal_eval(row[rule_order_csv])
        encoding_scheme_name = row[encoding_scheme_csv]
        edge_weight = row[encoding_scheme_csv] == "edge_weight"
        mutation_rate = float(row[mutation_rate_csv])
        env_repetition = int(row[environment_repetitions_csv])
        population_size = int(row[pop_size_csv])
        budget = int(row[budget_csv])
        env = map_name


        matrix = matrix / experments_size
        max_val = np.max(matrix)
        # Append new data
        key = (env)
        if key not in data:
            # Key is not present, add the data
            new_entry = {key: max_val}
            data.update(new_entry)
        else:
            # Key exists, compare the max_val and replace if necessary
            existing_max_val = data[key]
            if max_val > existing_max_val:
                data[key] = max_val
        matrix = np.transpose(matrix)

        matrix_with_info.append((matrix,env,num_agents,encoding_scheme_name,mutation_rate,env_repetition))


############################################
############################################
## DEFAULT CASE
############################################
############################################

folder_path = folder_path +"/Default"
# List all files in the folder
file_list = os.listdir(folder_path)

# Filter and sort the file list based on the 'i' value
file_list = sorted(file_list, key=lambda x: int(x.split("_")[-1].split(".")[0]))

experments_size = 250
current_experiment = []
experments_sums = []

def process_group(matrix_group):
    group_sum = np.sum(matrix_group, axis=0)
    return group_sum

for filename in file_list:
    matrix = np.loadtxt(os.path.join(folder_path, filename))  # Adjust loading based on your matrix format
    current_experiment.append(matrix)
    
    if len(current_experiment) == experments_size:
        experments_sums.append(process_group(current_experiment))
        current_experiment = []


# Process any remaining matrices in the last group
if current_experiment:
    print("ERROR")


print("Sums of each:")
for i, experments_sum in enumerate(experments_sums):
    print(f"experiment {i + 1} sum:\n{experments_sum}")

    for matrix,map, num_agents in zip(experments_sums,["random-32-32-20","empty-48-48","random-64-64-20"],[200,400,400]):
        env = map
        matrix = matrix / experments_size
        max_val = np.max(matrix)
         # Append new data
        key = (env)
        if key not in data:
            # Key is not present, add the data
            new_entry = {key: max_val}
            data.update(new_entry)
        else:
            # Key exists, compare the max_val and replace if necessary
            existing_max_val = data[key]
            if max_val > existing_max_val:
                data[key] = max_val
        matrix = np.transpose(matrix)
        
        matrix_with_info.append((matrix,env,num_agents,"default",0,0))

for matrix,env,num_agents,encoding_scheme_name,mutation_rate,env_repetition in matrix_with_info:
        # Create a figure and axes
        fig, ax = plt.subplots()
        heatmap = ax.imshow(matrix, cmap='GnBu', origin="lower", vmax=data[env])
        
        black_fields = load_obstacles(env)
        if dotbool:
            for field in black_fields:
                # ax.add_patch(plt.Rectangle((field[0]-0.5, field[1]-0.5), 1, 1, fill=True, color='black', alpha=1))
                if env == "random-64-64-20":
                    ax.plot(field[0]-0.05, field[1]+0.05, marker='o', markersize=3, color='black', alpha=0.8)
                else:
                    ax.plot(field[0]-0.05, field[1]+0.05, marker='o', markersize=4.5, color='black', alpha=0.8)
        # Add colorbar for reference
        # if encoding == "edge_weight":
        fig.colorbar(heatmap)
        # Remove x and y ticks
        ax.set_xticks([])
        ax.set_yticks([])
        # Add a title
    
        # plt.title(f"{env}", fontsize=17)

        if encoding_scheme_name == "default":
            plt.savefig(f"GA_Training_Benchmark_Maps/plots/{env}_{num_agents}_default.png")
        else:
            plt.savefig(f"GA_Training_Benchmark_Maps/plots/{env}_{num_agents}_{encoding_scheme_name}_{mutation_rate}_{env_repetition}.png")




print("Done")