import matplotlib.pyplot as plt

# Define a line style for the plots
line_style = '--'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

# Create some sample data
passage_best = [139.605, 199.302, 323.483]
passage_default = [137.436, 200.148, 328.397]
r1 = [4, 6, 8]

random_10_10_20_best = [94.042, 296.384, 890.753]
random_10_10_20_default = [93.608, 308.192, 917.771]
r2 = [10, 20, 30]

empty_10_10_best = [166.897, 578.515, 2950.809]
empty_10_10_default = [168.312, 573.606, 2968.412]
r3 = [20, 40, 60]

# Create the first plot
plt.plot(r1, passage_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r1, passage_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: passage')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r1[::])
plt.legend()
plt.show()

# Create the second plot
plt.plot(r2, random_10_10_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r2, random_10_10_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: random-10-10-20')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r2[::])
plt.legend()
plt.show()

# Create the third plot
plt.plot(r3, empty_10_10_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='best rule order', color="blue")
plt.plot(r3, empty_10_10_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default rule order', color="red")
plt.title('Map: empty-10-10')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r3[::])
plt.legend()
plt.show()
