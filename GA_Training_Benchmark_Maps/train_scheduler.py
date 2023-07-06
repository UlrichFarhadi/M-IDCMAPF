import subprocess
import os

command = ['python3', "GA_Training_Benchmark_Maps/train_benchmark.py"]

# Execute the command and capture the output
while True:
    subprocess.run(command)
    # Check if the flag file exists
    if os.path.exists('inner_script_complete.txt'):
        # Perform actions after the inner script is done
        print('Inner script is done!')
        # Remove the flag file
        os.remove('inner_script_complete.txt')
        # Exit the loop or continue with further processing
        break

