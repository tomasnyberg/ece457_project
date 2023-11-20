# Author: Tomas Nyberg (21111387)
# Co-operative & Adaptive Algorithms (ECE457A) - Project

from randomPath import randomPathFinding
from createGraph import create_campus_graph, dist_map
from VisualizeGraph import GraphVisualization

CAMPUS_GRAPH = create_campus_graph()
NODE_NAMES = ["CIF", "V1", "CMH", "NH", "E7", "MC", "PAC", "SLC", "QNC", "LIB", "DC", "E3", "EV3", "STC", "SCH"]

# One iteration of the random pathfinding algorithm
# Input: Graph in the NetworkX format
# Outputs:  [total path cost, path, weights]
# Example: (57, [1,5,4,3,2,1] [10,8,11,3,25])
def random_path(campus_graph):
    return randomPathFinding(campus_graph)

def iterate_random_algorithm(campus_graph, iterations = 100):
    assert iterations > 0, "Number of iterations must be greater than 0"
    best = [float('inf'), [], []]
    for it in range(iterations):
        current = random_path(campus_graph)
        if current[0] < best[0]:
            best = current
    return best

def visualize_random_path(campus_graph, iterations = 100):
    g = GraphVisualization()
    best_random = iterate_random_algorithm(CAMPUS_GRAPH, iterations)
    for i in range(len(best_random[1])):
        best_random[1][i] = NODE_NAMES[best_random[1][i]]
    g.create_network(best_random[1], best_random[2])
    g.visualize()

visualize_random_path(CAMPUS_GRAPH, 1000)



