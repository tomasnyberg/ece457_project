# Author: Franziska-Sophie Göttsch (21111390)
# Co-operative & Adaptive Algorithms (ECE457A) - Project
#
# Generate and randomly initialize a fully connected graph for solving a capacity based version of the Traveling Salesman Problem 
#
# Summary:
# This python file contains code to generate a fully conected graph of a certain size whith randomly initialized wheights for different time intervals.
# The graph is modeled using the Python library NetworkX.
# dist_map is based on actual distances between campus buildings (Data from Google Maps).
# The initial costs are generated based on the distance between two nodes and the random occupancy assigned to an edge at each time slot.

# ---------------------------------------------------------------------------------------------------------------------------------------
#                                                      Libraries
#----------------------------------------------------------------------------------------------------------------------------------------

import networkx as nx
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------------------------
#                                                  Global Variables
# ---------------------------------------------------------------------------------------------------------------------------------------

# stores the distances (in m) from one building on the UWaterloo campus to another
#          CIF V1	CMH	  NH   E7    MC	 PAC  SLC  QNC	LIB	 DC	  E3   EV3	STC	SCH                 IDs
dist_map = [[0, 430, 1130, 690, 750, 500, 380, 470, 570, 780, 590, 730, 900, 630, 930], # CIF       [0]
           [430, 0, 1120, 540, 860, 490, 320, 370, 470, 650, 640, 730, 660, 550, 820],  # V1        [1]
           [1130, 1120, 0, 600, 400, 650, 820, 740, 640, 490, 550, 400, 620, 560, 340], # CMH       [2]
           [690, 540, 600, 0, 490, 240, 330, 230, 140, 120, 340, 300, 200, 120, 290],   # NH        [3]
           [750, 860, 400, 490, 0, 370, 550, 500, 430, 440, 220, 190, 630, 380, 440],   # E7        [4]
           [500, 490, 650, 240, 370, 0, 180, 130, 110, 300, 150, 250, 450, 140, 440],   # MC        [5]
           [380, 320, 820, 330, 550, 180, 0, 90, 200, 420, 320, 430, 510, 270, 570],    # PAC       [6]
           [470, 370, 740, 230, 500, 130, 90, 0, 110, 330, 290, 360, 410, 190, 490],    # SLC       [7]
           [570, 470, 640, 140, 430, 110, 200, 110, 0, 220, 230, 270, 350, 70, 370],    # QNC       [8]
           [780, 650, 490, 120, 440, 300, 420, 330, 220, 0, 340, 240, 200, 160, 170],   # LIB (DP)  [9]
           [590, 640, 550, 340, 220, 150, 320, 290, 230, 340, 0, 170, 510, 210, 420],   # DC        [10]
           [730, 730, 400, 300, 190, 250, 430, 360, 270, 240, 170, 0, 440, 210, 270],   # E3        [11]
           [900, 660, 620, 200, 630, 450, 510, 410, 350, 200, 510, 440, 0, 330, 270],   # EV3       [12]
           [630, 550, 560, 120, 380, 140, 270, 190, 70, 160, 210, 210, 330, 0, 310],    # STC       [13]
           [930, 820, 340, 290, 440, 440, 570, 490, 370, 170, 420, 270, 270, 310, 0]]   # SCH       [14]
  
# stores the coordinates of each campus building, where QNC is the center of the coordinate system
# Note: The coordinates do not relate to any units (m, km, etc.), they were estimatet using the pixel coordinates of each building on a screenshot of Google Maps
#              [  x ,  y ]   Building   IDs
coordinates = [[-325,-515], # CIF       [0]
               [-513,-55],  # V1        [1]
               [738,115],   # CMH       [2]
               [50,156],    # NH        [3]
               [446,-244],  # E7        [4]
               [40,-123],   # MC        [5]
               [-175,-111], # PAC       [6]
               [-112,-78],  # SLC       [7]
               [0,0],       # QNC       [8]
               [188,187],   # LIB (DP)  [9]
               [227,-157],  # DC        [10]
               [326,-55],   # E3        [11]
               [65,382],    # EV3       [12]
               [78,82],     # STC       [13]
               [377,270]]   # SCH       [14]


# ---------------------------------------------------------------------------------------------------------------------------------------
#                                                CampusGraph Class
# ---------------------------------------------------------------------------------------------------------------------------------------

"""
Takes input parameters to generate a fully connected graph with n nodes of campus buildungs with weighted edges.
Each edge has n time slots with each a different weight.
The weight of an edge at a certain timeslot is determined based on the distance between the nodes and current occupancy

Arguments: 
- nr_of_nodes=15 {int} : The number of fully connected nodes in the final graph (ids of the nodes go from 0 to nr_of_nodes-1), default (and max) value is 15
- occupancy_range=(0,10) {(int,int)} : This range is used to randomly initialize the occupancy of an edge. Both, the upper and lower bound, are inclusive. 
Returns:
- {networkx.classes.graph.Graph} : Fully connected and initialized weighted graph
"""
def create_campus_graph(nr_of_nodes=15, occupancy_range=(0,10)):
    n = nr_of_nodes
    if nr_of_nodes > 15: # currently the max number of nodes is 15
        n = 15
    elif nr_of_nodes < 0: # number of nodes has to be positive
        n = 0

    G = nx.complete_graph(n) # creates a fully connected graph of type nx.Graph()
    initialize_weigths(G, n, occupancy_range) 

    return G

"""
Based on occupancy and distance of an edge, its weight is generated.
Takes the range for initial occupancies to generate random integer vectors representing the occupancy of an edge at each time slot

Arguments:
- G {networkx.classes.graph.Graph} : Fully connected graph, contains only the nodes and empty edges
- n {int} : Number of nodes in the graph (number of nodes equals the number of time slots)
- occupancy_range=(0,10) {(int,int)} : This range is used to randomly initialize the occupancy of an edge. Both, the upper and lower bound, are inclusive. 
"""
def initialize_weigths(G, n, occupancy_range):
    for edge in list(G.edges): # iterate through each edge
        node1, node2 = edge
        occupancies = np.random.randint(occupancy_range[0], occupancy_range[1]+1, size=n) # random occupancies
        weights = weight_function(dist_map[node1][node2], occupancies, n) # calculate actual weights based on weight function
        G.edges[edge]['occupancies'] = occupancies # add occupanciy vector as attribute to edge
        G.edges[edge]['weights'] = weights # add weight vector as attribute to edge

"""
Takes a distance (scalar) and occupancies (vector) to calculate the weights.
The higher the occupancy is, the higher the weight (depends on its squared value)

Arguments:
- dist {int} : distance in meters between the start and end node of th current edge
- occupancies {[int]} : stores the occupancy for each time slot of the current edge
- n {int} : Number of nodes in the graph (number of nodes equals the number of time slots)
Returns:
- {[int]} : Weight vector of the edge containing the weight for each time slot
"""
def weight_function(dist, occupancies, n):
    weigths = dist * (np.ones(n) + np.square(occupancies)) # dist*(1+occupancy^2)
    return weigths

# Example for a graph with 5 nodes and initial occupancies between 2 and 5
# G = create_campus_graph(5,(2,5)) # create graph
# print(G.nodes)                   # prints the id of each node in the graph
# print(G.edges)                   # prints every edge of the graph as a list of tuples with start and end node
# print(G.edges[1,2]['weights'])   # prints the weight vector for the edge between the nodes with the ids 1 and 2