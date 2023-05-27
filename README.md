# M-IDCMAPF

Code for the _M-IDCMAPF_ algorithm.

To run:

Install the libraries in the requirements.txt file.

In the main file there are some examples. One that runs a live simulation of the map _random-32-32-20_ with 100 agents, using the default rule order.

Then there is another experiment in the main file where _random-32-32-20_ is run with 200 agents for the 25 benchmark scenarios (10 times each). This is done with default rule order, best rule order, best rule order + node vector encoding, and best rule order + edge weight encoding.
The results are thereafter compared using two-sample t-test and the p-value is printed for each comparison


