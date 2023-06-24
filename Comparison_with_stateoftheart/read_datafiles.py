import csv


def calc_soc_DCMAPF(filename, map_name, num_agents):
    total_soc = 0
    count = 0

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['map_name'] == map_name and int(row['num_agents']) == num_agents and row['solved'] == 'True':
                total_soc += int(row['soc'])
                count += 1
    #print("scens: ", count)
    if count > 0:
        average_soc = total_soc / count
        return average_soc, (count / 25)
    else:
        return None, None
    
def calc_soc_EECBS(filename, map_name, num_agents):
    count = 0
    total_soc = 0

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if (
                row['map_name'] == map_name
                and int(row['num_agents']) == num_agents
                and int(row['solved']) == 1
            ):
                total_soc += int(row['soc'])
                count += 1
    #print("scens: ", count)
    if count > 0:
        average_soc = total_soc / count
        return average_soc, (count / 25)
    else:
        return None, None

def calc_soc_PIBT(filename, map_name, num_agents):
    count = 0
    total_soc = 0

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (
                row['map_name'] == map_name
                and int(row['num_agents']) == num_agents
                and int(row['solved']) == 1
            ):
                total_soc += int(row['soc'])
                count += 1
    #print("scens: ", count)
    if count > 0:
        average_soc = total_soc / count
        return average_soc, (count / 25)
    else:
        return None, None
import csv

def calc_soc_CBS(filename, map_name, num_agents):
    count = 0
    total_soc = 0

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['map_name'] == map_name and int(row['num_agents']) == num_agents and int(row['solved']) == 1:
                soc = int(row['soc'])
                total_soc += soc
                count += 1
    #print("scens: ", count)
    if count > 0:
        average_soc = total_soc / count
        return average_soc, (count / 25)
    else:
        return None, None

def calc_soc(map_name, num_agents, method_name):
    filename = 'Comparison_with_stateoftheart/' + method_name + ".csv"
    soc = None
    if method_name == "DCMAPF" or method_name == "IDCMAPF":
        soc = calc_soc_DCMAPF(filename, map_name, num_agents)
    if method_name == "EECBS":
        soc = calc_soc_EECBS(filename, map_name, num_agents)
    if method_name == "CBS":
        soc = calc_soc_CBS(filename, map_name, num_agents)
    if method_name == "PIBT" or method_name == "PIBT_PLUS":
        soc = calc_soc_PIBT(filename, map_name, num_agents)
    return soc




# method_name = "CBS"
# map_name = 'random-32-32-20.map'
# num_agents = 100

# average_soc, success_rate = calc_soc(map_name, num_agents, method_name)
# if average_soc is not None:
#     print(f"The average SOC for map '{map_name}' with {num_agents} agents is: {average_soc} with Success Rate: {success_rate}")
# else:
#     print("No data available for the specified criteria.")

socs = []
succ = []
map_name = 'ost003d.map'
method_name = "IDCMAPF"
densities = [50,100,150,200,250,300]
for num_agents in densities:
    average_soc, success_rate = calc_soc(map_name, num_agents, method_name)
    if average_soc is not None:
        socs.append(average_soc)
        succ.append(success_rate)
    else:
        socs.append(None)
        succ.append(0)
print("For the map: " + map_name + " with method: " + method_name + ":")
print(socs)
print(succ)
print(densities)