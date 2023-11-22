# The following is an example of use case
import numpy as np

from aco import AntColony
from createGraph import dist_map

# Sending format into array
distances = np.array(dist_map)
# Limit is from 0 to 14, you can add them in any order 14, 0
ant_colony = AntColony(distances, 13, 15)
shortest_path, costs = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
print ("cost: {}".format(costs))