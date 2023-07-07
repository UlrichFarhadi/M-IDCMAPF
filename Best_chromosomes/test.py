import numpy as np
import matplotlib.pyplot as plt

sep_val = 100
width = 50


x = np.array([1000,2000,3000])
den = [4,6,8]
names = ['Value 1', 'Value 2', 'Value 3']

data1 = np.array([np.random.normal(loc=0.5,size=100),np.random.normal(loc=1.5,size=100),np.random.normal(loc=2,size=100)]).T
data2 = np.array([np.random.normal(loc=2.5,size=100),np.random.normal(loc=0.75,size=100),np.random.normal(loc=0.25,size=100)]).T
plt.figure()
box1 = plt.boxplot(data1, 0, '', positions=x-sep_val, widths=width, patch_artist=True, boxprops=dict(facecolor='skyblue'))
box2 = plt.boxplot(data2, 0, '', positions=x, widths=width, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
box3 = plt.boxplot(data2, 0, '', positions=x+sep_val, widths=width, patch_artist=True, boxprops=dict(facecolor='lightpink'))


plt.xticks(x, names)

legends = [box1["boxes"][0], box2["boxes"][0], box3["boxes"][0]]
labels = ['Data 1', 'Data 2', 'Data 3']
plt.legend(legends, labels, loc='upper right')

plt.show()
