import numpy as np
import random
from scipy.interpolate import RectBivariateSpline

def generate_points(R, C, k_R, k_C, default_value=None):
    points = []
    pt_tmp = 0
    for i in range(R//k_R):
        row_points = []
        for j in range(C//k_C):
            if default_value is None:
                row_points.append(random.random()) # Value between 0 and 1
            else:       
                #row_points.append(default_value)
                row_points.append(pt_tmp)
                pt_tmp += 1
        points.append(row_points)
    return points

def interpolate_points(points, X, Y):
    # Convert points to a numpy array
    points = np.array(points)

    # Get the shape of the points array
    R, C = points.shape

    # Create a new set of points with spacing of 1
    new_x = np.linspace(0, 1, num=X)
    new_y = np.linspace(0, 1, num=Y)

    # Create a bivariate spline for interpolating the points
    #print(np.arange(0, R))
    #print(np.arange(0, C))
    interp_func = RectBivariateSpline(np.arange(0, R), np.arange(0, C), points)

    # Evaluate the interpolated function on the new set of points
    interpolated_points = interp_func(new_x, new_y)

    return interpolated_points


# Define the grid dimensions and spacing factor
R = 12  # number of rows
C = 12  # number of columns
k_R = 3  # spacing factor for rows
k_C = 3  # spacing factor for cols

# Generate the points
#points = generate_points(R, C, k_R, k_C, default_value=0.5)
#print(points)

# Define the dimensions of the output grid
X = 12  # number of rows
Y = 12  # number of columns

# Interpolate the points to generate the output grid
points = [[0, 0, 0, 0], [1, 1, 1, 1.0], [2, 2, 2, 2], [3, 3, 3, 3]]
interpolated_points = interpolate_points(points, X, Y)

# Print the interpolated points
print(interpolated_points)
print(interpolated_points.shape)
