import subprocess
import os

python_ver = 'python3'
command = [python_ver, "GA_Training_Benchmark_Maps/train_benchmark.py"]
command_ttest = [python_ver, "GA_Training_Benchmark_Maps/ttest_benchmark_maps.py"]

# Execute the command and capture the output
while True:
    subprocess.run(command)
    # Check if the flag file exists
    if os.path.exists('GA_Training_Benchmark_Maps/inner_script_complete.txt'):
        # Perform actions after the inner script is done
        print('Inner script is done!')
        # Remove the flag file
        os.remove('GA_Training_Benchmark_Maps/inner_script_complete.txt')
        # Exit the loop or continue with further processing
        print("Running Statistical Test")
        subprocess.run(command_ttest)
        break

