import matplotlib.pyplot as plt

# Define a line style for the plots
line_style = '--'

# Define the marker size
marker_size = 6

# Define the marker edge width
marker_edge_width = 2

# Create some sample data
random_10_10_20_best = [96.34, 285.334, 771.712]
random_10_10_20_default = [98.567, 299.151, 902.903]
r1 = [10, 20, 30]

empty_10_10_best = [180.251, 691.38, 2673.544]
empty_10_10_default = [166.849, 573.348, 2979.616]
r2 = [20, 40, 60]

random_32_32_20_best = [3094.888, 5749.944, 10660.932]
random_32_32_20_default = [3121.272, 6246.948, 12447.152]
r3 = [100, 150, 200]

y_bottom = 0.75
y_top = 1.01

# Create the first plot
plt.plot(r1, random_10_10_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='optimized map edges', color="blue")
plt.plot(r1, random_10_10_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default map edges', color="red")
plt.title('Map: random_10_10_20')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r1[::])
#plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()

# Create the second plot
plt.plot(r2, empty_10_10_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='optimized map edges', color="blue")
plt.plot(r2, empty_10_10_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default map edges', color="red")
plt.title('Map: empty_10_10')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r2[::])
#plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()

# Create the third plot
plt.plot(r3, random_32_32_20_best, marker='o', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='optimized map edges', color="blue")
plt.plot(r3, random_32_32_20_default, marker='D', linestyle=line_style, linewidth=2, markersize=marker_size, markeredgewidth=marker_edge_width, label='default map edges', color="red")
plt.title('Map: random_32_32_20')
plt.xlabel('Number of robots')
plt.ylabel('Sum of costs')
plt.xticks(r3[::])
#plt.ylim((y_bottom, y_top))
plt.legend()
plt.show()
