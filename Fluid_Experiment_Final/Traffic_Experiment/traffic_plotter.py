import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# # Get the path of the current script
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Add the parent directory of the current script to the Python path
# parent_dir = os.path.abspath(os.path.join(script_dir, '../..'))
# sys.path.append(parent_dir)

dotbool = True

# Load data
# Folder path containing the .txt files

# folder_paths = ["best_no_chromo", "def_no_chromo", "dir_best", "weight_best"]
# titles = ["Best Rule Order", "Default Rule Order", "Node Vector Encoding", "Edge Weight Encoding"]
# divisor = 250

# folder_paths = ["random_default", "random_dir", "random_weight"]
# titles = ["Default Rule Order", "Node Vector Encoding", "Edge Weight Encoding"]
# divisor = 250

# titles = ["Default Rule Order", "Node Vector Encoding", "Edge Weight Encoding"]
# folder_paths = ["empty_default", "empty_dir", "empty_weight"]
# divisor = 1000
# dotbool = False

# titles = ["Default Rule Order", "Node Vector Encoding", "Edge Weight Encoding"]
# folder_paths = ["fluid_default", "fluid_dir", "fluid_weight"]
# divisor = 1000
# dotbool = False





for folder_path, title in zip(folder_paths, titles):

    #folder_path = "weight_best"

    # Initialize an empty sum matrix
    sum_matrix = None

    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a .txt file
        if file_name.endswith(".txt"):
            # Load the matrix from the file
            file_path = os.path.join(folder_path, file_name)
            matrix = np.loadtxt(file_path)
            
            # Sum the matrices
            if sum_matrix is None:
                sum_matrix = matrix
            else:
                sum_matrix += matrix

    sum_matrix = sum_matrix / divisor

    # Plot the heatmap
    #plt.imshow(normalized_matrix, cmap='hot')
    matrix = np.transpose(sum_matrix)

    # Create a figure and axes
    fig, ax = plt.subplots()


    #plt.imshow(matrix, cmap='YlGnBu', origin="lower")
    heatmap = ax.imshow(matrix, cmap='GnBu', origin="lower")

    black_fields = [(0, 0), (1, 0), (15, 0), (18, 0), (28, 0), (0, 1), (1, 1), (3, 1), (6, 1), (7, 1), (9, 1), (11, 1), (12, 1), (18, 1), (27, 1), (0, 2), (5, 2), (10, 2), (15, 2), (17, 2), (19, 2), (23, 2), (30, 2), (31, 2), (0, 3), (3, 3), (4, 3), (11, 3), (15, 3), (19, 3), (29, 3), (30, 3), (31, 3), (2, 4), (5, 4), (8, 4), (1, 5), (8, 5), (10, 5), (20, 5), (21, 5), (31, 5), (16, 6), (25, 6), (28, 6), (31, 6), (17, 7), (21, 7), (23, 7), (26, 7), (28, 7), (7, 8), (13, 8), (18, 8), (22, 8), (24, 8), (26, 8), (27, 8), (2, 9), (4, 9), (7, 9), (12, 9), (19, 9), (30, 9), (7, 10), (9, 10), (18, 10), (21, 10), (22, 10), (23, 10), (26, 10), (27, 10), (28, 10), (1, 11), (3, 11), (12, 11), (22, 11), (23, 11), (25, 11), (29, 11), (6, 12), (10, 12), (13, 12), (16, 12), (18, 12), (22, 12), (26, 12), (0, 13), (10, 13), (19, 13), (22, 13), (29, 13), (30, 13), (31, 13), (1, 14), (8, 14), (9, 14), (10, 14), (13, 14), (15, 14), (18, 14), (20, 14), (23, 14), (24, 14), (29, 14), (30, 14), (31, 14), (2, 15), (6, 15), (15, 15), (20, 15), (23, 15), (24, 15), (25, 15), (30, 15), (8, 16), (13, 16), (15, 16), (17, 16), (20, 16), (3, 17), (4, 17), (5, 17), (13, 17), (23, 17), (1, 18), (18, 18), (20, 18), (26, 18), (30, 18), (2, 19), (8, 19), (10, 19), (12, 19), (13, 19), (15, 19), (26, 19), (12, 20), (18, 20), (20, 20), (22, 20), (30, 20), (0, 21), (2, 21), (12, 21), (14, 21), (22, 21), (26, 21), (2, 22), (4, 22), (17, 22), (19, 22), (27, 22), (28, 22), (6, 23), (16, 23), (24, 23), (26, 23), (1, 24), (5, 24), (21, 24), (22, 24), (26, 24), (29, 24), (6, 25), (9, 25), (10, 25), (19, 25), (27, 25), (31, 25), (6, 26), (9, 26), (11, 26), (14, 26), (15, 26), (22, 26), (27, 26), (30, 26), (31, 26), (1, 27), (2, 27), (14, 27), (15, 27), (17, 27), (24, 27), (27, 27), (5, 28), (7, 28), (18, 28), (29, 28), (14, 29), (23, 29), (24, 29), (28, 29), (0, 30), (4, 30), (6, 30), (7, 30), (19, 30), (21, 30), (25, 30), (10, 31), (17, 31), (21, 31), (23, 31)]

    if dotbool:
        for field in black_fields:
            #ax.add_patch(plt.Rectangle((field[0]-0.5, field[1]-0.5), 1, 1, fill=True, color='black', alpha=0.05))
            ax.plot(field[0], field[1], marker='o', markersize=2, color='black', alpha=0.4)

    # Add colorbar for reference
    fig.colorbar(heatmap)
    # Add a title
    plt.title(title, fontsize=17)

    # Show the plot
    plt.show()

