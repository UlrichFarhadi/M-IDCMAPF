import csv
from statistics import mean

# filename = "Tuning_data_ga/edge_weight/validator_test.csv"
# encoding = "Edge weight" 
filename = "Tuning_data_ga/node_vector/validator_test.csv"
encoding = "Node vector"

title_size = 20
xlabel_size = 15
ylabel_size = 15
scalelabel_size = 15

#colormap = 'binary'
colormap = 'GnBu'
save = True

soc_list = []
span_list = []
pop_size_list = []
mutation_rate = []
rep_list = []
chromosome_list = []


with open(filename, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        pop_size_list.append(int(row[0]))
        mutation_rate.append(float(row[1]))
        rep_list.append(int(row[2]))
        soc_list.append(float(row[3]))
        span_list.append(float(row[4]))
        chromosome_list.append(row[5])

print(max(soc_list))
temp = list(soc_list)
for _ in range(10):
    idx = soc_list.index(min(temp))
    print(f"pop size: {pop_size_list[idx]}, mutation rate: {mutation_rate[idx]}, and repetition {rep_list[idx]} provides the lowest soc: {soc_list[idx]} and span {span_list[idx]}")
    temp.pop(temp.index(min(temp)))

for pop in [30,40,50]:
    temp= []
    for i, ele in enumerate(pop_size_list):
        if ele == pop:
            temp.append(soc_list[i])
    print(f"pop {pop} has a mean som of {mean(temp)}")



for mut in [0.05, 0.10, 0.15]:
    temp= []
    for i, ele in enumerate(mutation_rate):
        if ele == mut:
            temp.append(soc_list[i])
    print(f"mutation rate {mut} has a mean som of {mean(temp)}")


for rep in [5, 10, 15, 20]:
    temp= []
    for i, ele in enumerate(rep_list):
        if ele == rep:
            temp.append(soc_list[i])
    print(f"repetition {rep} has a mean som of {mean(temp)}")


import matplotlib.pyplot as plt
import numpy as np

for mutation_rate_value in [0.05, 0.10, 0.15]:
    pop = [30,40,50]
    rep = [5,10,15,20]
    data = np.zeros((3, 4))
    

    def find_indices(lst, value):
        return [index for index, element in enumerate(lst) if element == value]

    def find_common_values(list1, list2, mutation_list, mutation_rate):
        indices = []
        for value in list1:
            if value in list2:
                if mutation_list[value] == mutation_rate:
                    indices.append(value)
        return indices

    for x, i in enumerate(pop):
        p_idx = find_indices(pop_size_list,i)
        for y, r in enumerate(rep):
            r_idx = find_indices(rep_list,r)
            indices = find_common_values(p_idx,r_idx,mutation_rate,mutation_rate_value )
            soc = []
            for idx in indices:
                soc.append(soc_list[idx])
            if len(soc) != 15:
                print("ERROR")
            data[x,y] = mean(soc)


    x,y = rep,pop

    # Convert data to a numpy array
    data = np.array(data)

    # Plot the heatmap
    plt.imshow(data, cmap=colormap, interpolation='nearest')

    # Set labels and ticks
    plt.xticks(range(len(x)), x)
    plt.yticks(range(len(y)), y)
    plt.xlabel('Environment repetitions', fontsize=xlabel_size)
    plt.ylabel('Population size', fontsize=ylabel_size)
    plt.title(f"Mutation rate: {mutation_rate_value}", fontsize=title_size)

    # Add a colorbar
    colorbar = plt.colorbar()
    colorbar.set_label('Sum of costs', fontsize=scalelabel_size)  # Add a label to the colorbar

    # Display the plot
    if save:
        plt.savefig("Tuning_data_ga/Plots/" + encoding + "_" + str(mutation_rate_value) + ".png")
    plt.show()