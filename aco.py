# Acknowledge to project "Ant Colony Optimization Algorithm using Python": https://github.com/Akavall/AntColonyOptimization
import numpy as np
from numpy.random import choice as np_choice


class AntColony(object):

    def __init__(self, distances, campus_graph):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Distance uses the example provided by Franziska-Sophie
            campus_graph = provides list of nodes and edges from the list provided by Franziska-Sophie
            number_ants (int): Number of ants running per iteration 
            best_ants (int): Number of best ants who deposit pheromone 
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

            Parameters only require distances and campus graph
        Example:
            ant_colony = AntColony(distances, campus_graph)          
        """
        # All these values are standard process for ant algorithm
        self.distances = distances
        self.campus_graph = campus_graph
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_indexes = range(len(distances))
        self.number_ants = 1
        self.best_ants = 1
        self.number_iterations = 100
        self.decay = 0.95
        self.alpha = 1
        self.beta = 1

    def run(self):
        shortest_path = None
        # To indicate that no value has been calculated yet
        # Any calculated path would be less than the placeholder value.
        # Only positive infinite values
        all_time_shortest_path = ("placeholder", np.inf)
        for _ in range(self.number_iterations):
            all_paths = self.generate_all_paths()

            self.spread_pheromone(all_paths, self.best_ants)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay

        shortest_path = all_time_shortest_path[0]
        best_path = self.edges_to_nodes_ordered(shortest_path)
        weights = self.prepare_weights(best_path)
        sum_weight = sum(weights)
        return sum_weight, best_path, weights 
    # Spread pheromones from ants

    def spread_pheromone(self, all_paths, best_ants):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, path_distance in sorted_paths[:best_ants]:
            for move in path:
                if path_distance != 0:
                    self.pheromone[move] += 1.0 / self.distances[move]
                else:
                    self.pheromone[move] += 1.0
    # Generates the path distance available. Checks distances

    def generate_path_distance(self, path):
        total_dist = 0
        for item in path:
            total_dist += self.distances[item]
        return total_dist

    def generate_all_paths(self):
        all_paths = []
        # example_node = [0,1,2,3,4]
        all_nodes = list(self.campus_graph.nodes)
        for i in range(self.number_ants):
            # randomly select a starting node
            node_choice = np_choice(all_nodes)
            path = self.generate_path(node_choice)
            all_paths.append((path, self.generate_path_distance(path)))
        return all_paths
    # Generates a single path
    def generate_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        previous = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(
                self.pheromone[previous], self.distances[previous], visited)
            path.append((previous, move))
            previous = move
            visited.add(move)

        path.append((previous, start))
        return path
    # It generates the reciprocal of the path
    def generate_reciprocal(self, path_distance):
        reciprocal_array = np.zeros_like(path_distance, dtype=float)
        for i in range(path_distance.shape[0]):
            if path_distance[i] != 0:
                reciprocal_array[i] = 1 / path_distance[i]
            else:
                reciprocal_array[i] = 0
        return reciprocal_array

    def pick_move(self, pheromone, path_distance, visited):
        pheromone = np.copy(pheromone)

        pheromone[list(visited)] = 0
        visibility = self.generate_reciprocal(path_distance)

        row = pheromone ** self.alpha * (visibility ** self.beta)

        norm_row = row / row.sum()
        # Randomly choose another node to move
        move = np_choice(self.all_indexes, 1, p=norm_row)[0]
        return move

    # Makes the code into the required format
    def edges_to_nodes_ordered(self, edge_list):
        array = []
        counter = 0
        for edge in edge_list:
            x, y = edge
            if (counter == 0):
                array.append(x)
                array.append(y)
            else:
                array.append(y)
            counter += 1
        return array

    # From random path nodes - Updated to current code
    def prepare_weights(self, best_path):
        weights = []
        previous_node = best_path[0]
        current_node = 0
        step = 0

        for i in range(1, len(best_path)):
            current_node = best_path[i]

            new_weight = self.campus_graph.edges[previous_node,
                                                 current_node]['weights'][step]
            weights.append(new_weight)

            previous_node = current_node
            step += 1

        return weights

    # Example usage:
    # -- code --
    """ 
    The following is an example of how to implement the algorithm in our code
    from aco import AntColony
    from createGraph import dist_map, create_campus_graph

    campus_graph = create_campus_graph()
    # Sending format into array
    distances = np.array(dist_map)
    # It selects random nodes as any start, then it follows the shortest path and returns best result
    ant_colony = AntColony(distances, campus_graph)
    shortest_path, weight, cost = ant_colony.run()
    print("shorted_path: {}".format(shortest_path))
    print("weights: {}".format(weight))
    print("cost: {}".format(cost))
    """
