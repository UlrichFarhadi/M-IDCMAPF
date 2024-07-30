# M-IDCMAPF

This repository contains the code for the M-IDCMAPF algorithm, created by Ulrich Farhadi and Henning Hess (https://github.com/henning998).

Below is an example video:

[![M-IDCMAPF](https://img.youtube.com/vi/5QSAsHZA1K8/0.jpg)](https://www.youtube.com/watch?v=5QSAsHZA1K8)


## How to Run
This guide will walk you throuch creating your own map, evolving path costs and getting statistical results to see if it was possible to obtain optimized edge weights for the given map.

1. Install the required libraries listed in the `requirements.txt` file. The python version used in this project is `Python 3.11`

2. Create your environment map and place it in the "Environments folder". In this folder, an experiment map "experiment_map.map" can be found. We will be using this throughout this guide.

3. Run the Visualization_of_single_run to see how everything looks. The parameters can be changed in the function "run_one_sim" to increase or decrease the amount of agents or change the map to another of your liking.

4. Setup the cases, hyperparameters and budget for the experiment runs in the GA_Training_Benchmark_Maps folder, open the cases.csv file. It will look like this:
case_nr,map_name,num_agents,rule_order,encoding_scheme,mutation_rate,environment_repetitions,pop_size,budget,finished_amt
experiment_map,40,"[0,1,2,3,4,5,6]",edge_weight,0.1,5,50,10000,3
experiment_map,40,"[0,1,2,3,4,5,6]",node_vector,0.1,5,50,10000,3

Here we run 2 experiments, one with edge_weight encoding and one with node_vector on the "experiment_map" map with 40 agents. We are using the default rule order "0,1,2,3,4,5,6" and mutation rate of 0.1 with 5 resamples as described in the paper. To make the process short, we use a budget of 10.000 fitness evaluations for each experiment. We repeat each experiment 3 times (described by the finished_amt parameter). This will yield a total of 6 chromosomes, 3 for edge weight and 3 for node vector. These chromosomes are stored in "chromosomes.csv". 

Then you need to run the train_scheduler.py to start the evolution process. BUT IMPORTANTLY: Before running this file you need to clear the contents of chromosomes.csv and results.csv. These files are not automatically cleared because we want the posibillity of stopping the script from running, and resume it at a later point. To resume it you just need to run the train_scheduler.py again and it will continue where it left off (but restarting any single run that was not finished, in the case above, a single run corresponds to any of the 6 runs defined in the cases.csv).

6. TODO: Update code for the traffic plot so it can be run immeidately after the steps above for the given configuration.

## License

This project is licensed under the [MIT License](LICENSE).
