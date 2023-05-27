import matplotlib.pyplot as plt

# Define a line style for the plots
line_style = '--'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

# Create some sample data
random_32_32_20_best = [3125.616, 6248.128, 12520.272]
random_32_32_20_default = [3190.528, 6489.756, 13045.504]
r1 = [100, 150, 200]

empty_48_48_best = [6855.108, 15951.6, 36680.108]
empty_48_48_default = [6859.992, 16028.824, 37615.696]
r2 = [200, 400, 600]


# Create the first plot
plt.plot(r1, random_32_32_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r1, random_32_32_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: random-32-32-20')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r1[::])
plt.legend()
plt.show()

# Create the second plot
plt.plot(r2, empty_48_48_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r2, empty_48_48_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: empty-48-48')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r2[::])
plt.legend()
plt.show()
