import csv
from statistics import mean

filename = "Tuning_data_ga/edge_weight/validator_test.csv"  

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

    def find_common_value(list1, list2, mutation_list, mutation_rate):
        for value in list1:
            if value in list2:
                if mutation_list[value] == mutation_rate:
                    return value

    for x, i in enumerate(pop):
        p_idx = find_indices(pop_size_list,i)
        for y, r in enumerate(rep):
            r_idx = find_indices(rep_list,r)
            idx = find_common_value(p_idx,r_idx,mutation_rate,mutation_rate_value )
            data[x,y] = soc_list[idx]


    x,y = rep,pop

    # Convert data to a numpy array
    data = np.array(data)

    # Plot the heatmap
    plt.imshow(data, cmap='hot', interpolation='nearest')

    # Set labels and ticks
    plt.xticks(range(len(x)), x)
    plt.yticks(range(len(y)), y)
    plt.xlabel('Repetition')
    plt.ylabel('Population size')
    plt.title(f"With mutation rate: {mutation_rate_value}")

    # Add a colorbar
    plt.colorbar()

    # Display the plot
    plt.show()