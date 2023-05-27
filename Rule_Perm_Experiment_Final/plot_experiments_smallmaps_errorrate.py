import matplotlib.pyplot as plt

# Define a line style for the plots
line_style = '--'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

# Create some sample data
passage_best = [1-0.036, 1-0.061, 1-0.211]
passage_default = [1-0.041, 1-0.066, 1-0.207]
r1 = [4, 6, 8]

random_10_10_20_best = [1-0, 1-0, 1-0.002]
random_10_10_20_default = [1-0, 1-0, 1-0.001]
r2 = [10, 20, 30]

empty_10_10_best = [1-0.001, 1-0.001, 1-0.019]
empty_10_10_default = [1-0.001, 1-0.001, 1-0.02]
r3 = [20, 40, 60]

y_bottom = 0.75
y_top = 1.01

# Create the first plot
plt.plot(r1, passage_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r1, passage_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: passage')
plt.xlabel('Number of robots')
plt.ylabel('Success rate')
plt.xticks(r1[::])
plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()

# Create the second plot
plt.plot(r2, random_10_10_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r2, random_10_10_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: random-10-10-20')
plt.xlabel('Number of robots')
plt.ylabel('Success rate')
plt.xticks(r2[::])
plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()

# Create the third plot
plt.plot(r3, empty_10_10_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r3, empty_10_10_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: empty-10-10')
plt.xlabel('Number of robots')
plt.ylabel('Success rate')
plt.xticks(r3[::])
plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()
