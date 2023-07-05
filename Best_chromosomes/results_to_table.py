import copy
from typing import List
import itertools
import numpy as np
from dask.distributed import Client, LocalCluster
from dask import delayed
import csv
import os
import sys
from statistics import mean
import matplotlib.pyplot as plt

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)


def print_latex_table_row(row):
    formatted_row = " & ".join(map(str, row))
    print(formatted_row + " ")

def read_csv_file(file_path):
    headline = ["Environment", "Agents" , "Encoding", "P-Value SOC", "P-Value Waits", "P-Value Conflicts", "Rule Order", "SOC (Optimized)" ,"Makespan (Optimized)", "Failrate (Optimized)", "Waits (Optimized)", "Conflicts (Optimized)", "SOC", "Makespan", "failrate", "waits", "conflicts"]
    print_latex_table_row(headline)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            print_latex_table_row(row)

def read_csv_file_soc(file_path):
    # Update the headline list with the desired columns
    headline = ["Map", "Agents", "P-Value", "SOC (Optimized)", "SOC","Improvement (%)"]
    print_latex_table_row(headline)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # Extract the specific columns from the row
            if row[0]=="fluid_test_smallscale":
                specific_columns = ["passage", row[1], round(float(row[3]),3), round(float(row[7]),2), round(float(row[-5]),2), f"{round((-(float(row[7])-float(row[-5]))/float(row[-5]))*100,2)} %"]
            else:
                specific_columns = [row[0], row[1], round(float(row[3]),3), round(float(row[7]),2), round(float(row[-5]),2), f"{round((-(float(row[7])-float(row[-5]))/float(row[-5]))*100,2)} %"]
            print_latex_table_row(specific_columns)


def read_csv_file_wait_conflict(file_path):
    # Update the headline list with the desired columns
    headline = ["Map", "Agents", "P-Value wait","wait (Optimized)", "wait","P-Value conflict", "conflict (Optimized)", "conflict"]
    print_latex_table_row(headline)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # Extract the specific columns from the row
            if row[0]=="fluid_test_smallscale":
                specific_columns = ["passage", row[1], round(float(row[4]),3), round(float(row[10]),2), round(float(row[15]),2), round(float(row[5]),3), round(float(row[11]),2), round(float(row[16]),2)]
            else:
                specific_columns = [row[0], row[1], round(float(row[4]),3), round(float(row[10]),2), round(float(row[15]),2), round(float(row[5]),3), round(float(row[11]),2), round(float(row[16]),2)]
            print_latex_table_row(specific_columns)



csv_file_path = "Best_chromosomes/results.csv"
# for i, idx in enumerate(["Environment", "Agents" , "Encoding", "P-Value SOC", "P-Value Waits", "P-Value Conflicts", "Rule Order", "SOC (Optimized)" ,"Makespan (Optimized)", "Failrate (Optimized)", "Waits (Optimized)", "Conflicts (Optimized)", "SOC", "Makespan", "failrate", "waits", "conflicts"]):
#     print(i,idx)
read_csv_file_soc(csv_file_path)
# read_csv_file_wait_conflict(csv_file_path)
