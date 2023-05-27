# Library imports
import sys
import os
import copy
import random
import numpy
from typing import List, Tuple, Callable

# Self made imports

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory of the current script to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir) 

from GA_TS import GA_travelling_salesman

ga_obj = GA_travelling_salesman()

ga_obj.run()

