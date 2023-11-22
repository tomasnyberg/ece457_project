import numpy as np

from aco import AntColony

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

ant_colony = AntColony(distances, 0, 3)
shortest_path, costs = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
print ("cost: {}".format(costs))