# Author: Patrick Kim (20871979)
# Co-operative & Adaptive Algorithms (ECE457A) - Project
#
# Create an algorithm to solve a capacity based version of the Traveling Salesman Problem using random selections

import networkx as nx
import numpy as np
import random


def randomPathFinding(G): # pass in graph after initializing it
    # copy index of nodes
    allNodes = list(G.nodes)

    #randomly select a starting node
    initialNode = random.choice(allNodes)
    allNodes.remove(initialNode)

    #init lists to return
    visitedNodes = []
    weights = []

    thisNode = initialNode
    step = 0

    visitedNodes.append(thisNode)
    #select a random node to travel from list until empty
    while len(allNodes) > 0:
        nextNode = random.choice(allNodes)
        allNodes.remove(nextNode)

        visitedNodes.append(nextNode)
        weights.append(G.edges[thisNode,nextNode]['weights'][step])

        #iterate to next nodes
        thisNode = nextNode
        step += 1

    #return back to initial node
    visitedNodes.append(initialNode)
    weights.append(G.edges[thisNode,initialNode]['weights'][step])

    #Example
    # Total path cost was 57, path was Nodes 1->5->4->3->2->1, weights were the 10,8,11,3,25 for those paths.
    #57, [1,5,4,3,2,1] [10,8,11,3,25
    return sum(weights), visitedNodes, weights






        
        








