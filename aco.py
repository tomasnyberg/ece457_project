# Acknowledge to https://github.com/Akavall/AntColonyOptimization
import random as rn
import numpy as np
from numpy.random import choice as np_choice


class AntColony(object):

    def __init__(self, distances, start, end):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.start = start
        self.end = end
        self.n_ants = 1
        self.n_best = 1
        self.n_iterations = 100
        self.decay = 0.95
        self.alpha = 1
        self.beta = 1

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()

            self.spread_pheronome(all_paths, self.n_best,
                                  shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay

        shortest_path, costs = all_time_shortest_path
        formatted_shortest = self.edges_to_nodes_ordered(shortest_path)

        return formatted_shortest, costs

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, path_distance in sorted_paths[:n_best]:
            for move in path:
                if path_distance != 0:
                    self.pheromone[move] += 1.0 / self.distances[move]
                else:
                    self.pheromone[move] += 1.0

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            # Update path for the start of the code
            path = self.gen_path(self.start)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(
                self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
            # If we reach to the end of the route we simply return the value
            if (prev == self.end):
                break

        path.append((prev, start))
        return path

    def get_reciprocal(self, path_distance):
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
        visibility = self.get_reciprocal(path_distance)

        row = pheromone ** self.alpha * (visibility ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
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
