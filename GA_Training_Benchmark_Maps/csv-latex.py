import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = "GA_Training_Benchmark_Maps/results.csv"

# Read CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Convert DataFrame to LaTeX table
latex_table = df.to_latex(index=False, escape=False)

# Print the LaTeX table code
print(latex_table)