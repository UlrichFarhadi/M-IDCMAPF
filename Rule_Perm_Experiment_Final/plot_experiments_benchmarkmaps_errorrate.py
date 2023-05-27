import matplotlib.pyplot as plt

# Define a line style for the plots
line_style = '--'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

# Create some sample data
random_32_32_20_best = [1-0.0, 1-0.004, 1-0.000]
random_32_32_20_default = [1-0.0, 1-0.008, 1-0.008]
r1 = [100, 150, 200]

empty_48_48_best = [1-0, 1-0, 1-0.004]
empty_48_48_default = [1-0, 1-0, 1-0.0]
r2 = [200, 400, 600]

y_bottom = 0.75
y_top = 1.01


# Create the first plot
plt.plot(r1, random_32_32_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r1, random_32_32_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: random-32-32-20')
plt.xlabel('Number of robots')
plt.ylabel('Success rate')
plt.xticks(r1[::])
plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()

# Create the second plot
plt.plot(r2, empty_48_48_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r2, empty_48_48_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: empty-48-48')
plt.xlabel('Number of robots')
plt.ylabel('Success rate')
plt.xticks(r2[::])
plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()
