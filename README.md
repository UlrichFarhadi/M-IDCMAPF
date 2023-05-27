# M-IDCMAPF

This repository contains the code for the M-IDCMAPF algorithm.

This below is an example video:

[![M-IDCMAPF](https://img.youtube.com/vi/5QSAsHZA1K8/0.jpg)](https://www.youtube.com/watch?v=5QSAsHZA1K8)


## How to Run

1. Install the required libraries listed in the `requirements.txt` file.

2. In the `main.py` file, you can find some examples:

    a. **Live Simulation Example**: This example runs a live simulation of the map `random-32-32-20` with 100 agents, using the default rule order.

    b. **Benchmark Experiment Example**: In this example, the map `random-32-32-20` is run with 200 agents for the 25 benchmark scenarios. Each scenario is run 10 times using different configurations:
    
        - Default rule order
        - Best rule order
        - Best rule order + node vector encoding
        - Best rule order + edge weight encoding
        
      The results from these experiments are then compared using a two-sample t-test, and the p-value for each comparison is printed.

Feel free to explore and modify the code to suit your needs. If you have any questions or issues, please open an issue in the repository.

## License

This project is licensed under the [MIT License](LICENSE).
