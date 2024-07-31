```plaintext
# M-IDCMAPF

This repository contains the code for the M-IDCMAPF algorithm, developed by Ulrich Farhadi and Henning Hess. For more information, visit [Henning Hess' GitHub](https://github.com/henning998).

Below is a demonstration video:

[![M-IDCMAPF](https://img.youtube.com/vi/5QSAsHZA1K8/0.jpg)](https://www.youtube.com/watch?v=5QSAsHZA1K8)

## How to Run

This guide will walk you through creating your own map, evolving path costs, and obtaining statistical results to determine if optimized edge weights for the given map were achieved.

1. **Install Required Libraries:**
   Install the libraries listed in the `requirements.txt` file. This project requires Python 3.11.

2. **Clone the Repository:**
   Use the following command to clone the repository. This command clones only the 'Clean' branch and limits the depth to avoid downloading unnecessary large branches:
   ```bash
   git clone --single-branch --branch Clean --depth 1 https://github.com/UlrichFarhadi/M-IDCMAPF.git
   ```

3. **Setup the Environment Map:**
   Create your environment map and place it in the "Environments" folder. You can use the provided "experiment_map.map" found in this folder for the guide.

4. **Visualize the Setup:**
   Run `Visualization_of_single_run.py` to visualize the setup. You can modify parameters in the `run_one_sim` function located in `main()` at the bottom of the `Visualization_of_single_run.py` file to adjust the number of agents or change the map.

5. **Configure Experiment Parameters:**
   Set up the cases, hyperparameters, and budget for the experiments in the `GA_Training_Benchmark_Maps/cases.csv` file. It should look like this:
   ```
   case_nr,map_name,num_agents,rule_order,encoding_scheme,mutation_rate,environment_repetitions,pop_size,budget,finished_amt
   experiment_map,15,"[0,1,2,3,4,5,6]",edge_weight,0.1,5,50,10000,3
   experiment_map,15,"[0,1,2,3,4,5,6]",node_vector,0.1,5,50,10000,3
   ```
   Here, we run two experiments: one with `edge_weight` encoding and one with `node_vector` encoding on the "experiment_map" with 15 agents. The default rule order is `[0,1,2,3,4,5,6]` and the mutation rate is 0.1, with 5 resamples and a population size of 50. We use a budget of 10,000 fitness evaluations per experiment and repeat each experiment 3 times. The results will be saved in `chromosomes.csv`.

6. **Generate Start and Target Configurations:**
   Generate the start and target configurations needed for evaluation. Run `Statistical_test_comparison/statistical_test_positions_generator.py` and set the following variables:
   - `map_name` to "experiment_map"
   - `number_of_agents` to 15 (or other numbers if applicable)
   
   This will create the necessary sets of start and target configurations.

7. **Run the Evolutionary Process:**
   Execute the evolutionary process by running `GA_Training_Benchmark_Maps/train_scheduler.py`. Before doing so, ensure that the `GA_Training_Benchmark_Maps/chromosomes.csv` file is cleared. This file is not automatically cleared to allow for the possibility of resuming training if stopped. To resume, simply run `train_scheduler.py` again. The process will continue from where it left off.

   Track the progress by monitoring the `cases.csv` file, where the `finished_amt` will count down to zero. When all `finished_amt` values are zero, the `train_scheduler` will perform statistical test comparisons automatically. Results will be saved in `GA_Training_Benchmark_Maps/results.csv`, which is reset automatically.

8. **Work in Progress:**
   Note that the code for traffic plots is not updated. The files `traffic_eval.py` and `traffic_plot.py` are still in use but require updates.

## License

This project is licensed under the [MIT License](LICENSE).
```