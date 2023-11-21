# Code updated from https://github.com/JPablo-bot/ACO-Metro-Mexico-City
import numpy as np
from math import sqrt

def euclidean_distance(p1, p2):
    sum = 0
    for i in range(len(p1)):
        sum += (p1[i] - p2[i]) ** 2
    d = sqrt(sum)
    return d


def initialize_pheromone(connections):
    return np.ones((len(connections), 1)) * 0.01


def calculate_visibility(connections, nodes):
    distances = np.zeros((len(connections), 1))
    visibility = np.zeros((len(connections), 1))

    for i in range(len(connections)):
        distances[i] = euclidean_distance(
            nodes[connections[i][0]], nodes[connections[i][1]])
        visibility[i] = 1 / distances[i]

    return visibility


def select_next_node(probability, select_line):
    select = np.random.rand()
    [camx, camy] = np.where(select < select_line)
    [antTox, antToy] = np.where(probability == probability[camx[0]])
    return int(antTox[0])


def update_pheromone(pheromone, all_ants, connections, all_distances):
    rho = 0.5  # Factor de evaporación
    Q = 1  # Factor de olvido

    for i in range(len(pheromone)):
        dTau = 0
        for j in range(len(all_ants)):
            ant_passed = False
            ant = np.array(all_ants[j])
            ant_location = np.zeros(np.shape(ant))
            ant_location = np.where(
                ant == connections[i][0], True, ant_location)
            ant_location = np.where(
                ant == connections[i][1], True, ant_location)
            for k in range(len(ant_location)):
                if ant_location[k][0] == 1 and ant_location[k][1] == 1:
                    ant_passed = True

            if ant_passed:
                dTau = dTau + (Q / all_distances[j])

        pheromone[i] = (1 - rho) * pheromone[i] + dTau

# Main ants algorithm, it adds start an end notes with connections and sends the best possible route
def ants_at_waterloo(start, end, nodes, connections):
    pheromone = initialize_pheromone(connections)
    visibility = calculate_visibility(connections, nodes)

    count = 0
    alpha = 1
    beta = 1
    min_nodes = len(nodes)

    while count < 10:
        n_ants = 50
        all_ants = []

        for _ in range(n_ants):
            current_ant = move_ant(
                start, end, alpha, beta, pheromone, visibility, connections, all_ants)
            all_ants.append(current_ant)

        all_distances = calculate_distances(all_ants, connections)

        update_pheromone(pheromone, all_ants, connections, all_distances)

        start, end, final_route, min_nodes, count, beta = update_parameters(
            start, end, all_distances, min_nodes, beta, count)

    return final_route


def move_ant(start, end, alpha, beta, pheromone, visibility, connections, all_ants):
    current_ant = []
    previous = -1

    while start != end:
        pheromone_route = np.where(connections[:, 0] == start)
        [indx, indy] = np.where(connections[pheromone_route, 1] == previous)

        if indy.size > 0:
            pheromone_route = np.delete(pheromone_route, int(indy))

        denominator = (
            (pheromone[pheromone_route[:]]**alpha) * (visibility[pheromone_route[:]]**beta))
        denominator = sum(denominator)

        probability = (
            ((pheromone[pheromone_route[:]]**alpha)*(visibility[pheromone_route[:]]**beta)) / denominator)

        select_line = calculate_selection_probability(probability)

        next_node = select_next_node(probability, select_line)

        current_ant.append([previous, start])
        previous = start
        start = int(connections[np.array(pheromone_route).T[next_node], 1])

    all_ants.append(current_ant)

    return current_ant


def calculate_distances(all_ants, connections):
    all_distances = []

    for i in range(len(all_ants)):
        index_distances = []
        for j in range(len(all_ants[i])):
            for k in range(len(connections)):
                if (all_ants[i][j] == connections[k]).all():
                    index_distances.append(k)
        all_distances.append(sum(index_distances))

    return all_distances


def update_parameters(start, end, all_distances, all_ants, min_nodes, beta, count):
    all_distances = np.array(all_distances)
    final_route = []

    for i in range(len(all_distances)):
        if all_distances[i] < min_nodes:
            min_nodes = all_distances[i]
            final_route = all_ants[i]
            count = 0

    count += 1

    if len(final_route) > min_nodes:
        beta -= 0.05
        count = 0

    return start, end, final_route, min_nodes, count, beta


def calculate_selection_probability(probability):
    select_line = []
    sum = 0

    for i in range(len(probability)):
        sum = sum + probability[i]
        select_line.append(sum)

    select_line = np.array(select_line)
    return select_line
