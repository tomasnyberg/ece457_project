# Author: Tomas Nyberg (21111387)
# Co-operative & Adaptive Algorithms (ECE457A) - Project

from randomPath import randomPathFinding
from createGraph import create_campus_graph, dist_map
from VisualizeGraph import GraphVisualization
from aco import AntColony
import numpy as np


CAMPUS_GRAPH = create_campus_graph()
NODE_NAMES = ["CIF", "V1", "CMH", "NH", "E7", "MC", "PAC",
              "SLC", "QNC", "LIB", "DC", "E3", "EV3", "STC", "SCH"]
POSITIONS = [(815, 280), (515, 860), (1000, 790), (1100, 840), (1275, 800), (1230, 940), (1340, 1040),
             (1300, 1150), (1310, 1440), (1470, 1200), (1525, 740), (1650, 870), (1715, 1285), (1800, 625), (2200, 1075)]


def random_path(campus_graph):
    """
    Executes one iteration of the random pathfinding algorithm on a given graph.

    Args:
        campus_graph (NetworkX.Graph): The graph on which to perform the pathfinding.

    Returns:
        tuple: A tuple containing the total path cost, the path as a list of node indices, and 
               the weights of the edges in the path. 
               Example: (57, [1, 5, 4, 3, 2, 1], [10, 8, 11, 3, 25])
    """
    return randomPathFinding(campus_graph)


def aco_path(campus_graph):
    """
    Executes one iteration of the ACO pathfinding algorithm on a given graph.

    Args:
        campus_graph (NetworkX.Graph): The graph on which to perform the pathfinding.

    Returns:
        tuple: A tuple containing the total path cost, the path as a list of node indices, and 
               the weights of the edges in the path. 
               Example: (57, [1, 5, 4, 3, 2, 1], [10, 8, 11, 3, 25])
    """
    # Convert dist_map to a numpy matrix
    return AntColony(np.array(dist_map), campus_graph).run()


def iterate_random_algorithm(campus_graph, iterations=100):
    """
    Iterates the random pathfinding algorithm a specified number of times and 
    finds the best path over all iterations.

    Args:
        campus_graph (NetworkX.Graph): The graph on which to perform the pathfinding.
        iterations (int): The number of iterations to perform. Default is 100.

    Returns:
        tuple: The best path found over all iterations, including its total cost,
               the path as a list of node indices, and the weights of the edges in the path.

    Raises:
        AssertionError: If the number of iterations is not greater than 0.
    """
    assert iterations > 0, "Number of iterations must be greater than 0"
    best = [float('inf'), [], []]
    for it in range(iterations):
        current = random_path(campus_graph)
        if current[0] < best[0]:
            best = current
    return best


def visualize_path(campus_graph, algorithm='random', iterations=100):
    """
    Visualizes the best path found using the random pathfinding algorithm over a 
    number of iterations.

    Args:
        campus_graph (NetworkX.Graph): The graph on which to perform the pathfinding.
        iterations (int): The number of iterations to perform. Default is 100.
    """
    g = GraphVisualization()
    total_cost, path, weights = iterate_random_algorithm(
        campus_graph, iterations) if algorithm == 'random' else aco_path(campus_graph)
    print(f"Total cost: {total_cost}, with the path {path}")
    print(f"Weights for this path: {weights}")
    g.create_network(path, POSITIONS, weights)
    g.visualize()


visualize_path(CAMPUS_GRAPH, algorithm='aco')
visualize_path(CAMPUS_GRAPH, algorithm='random', iterations=1)
