The following file contains the following code
1. Data - Information related with the mapping and data for the campus. It contains relevant information about the files from the elements.
2. aco.py - Metaheuristic algorithm learned in class, and updated with weights. Code references in the code.
3. createGraph.py - Document to create the nodes, edges, weights and occupancies from the map.
4. randomPath.py - Generates a random generated graph with the least efficient way of updating algorithms.
5. runExperiments - Provides evaluation and results for the algorithm and the results.

Updated ACO Algorithm

Ants randomly travel from a start location to an end location in all the buildings at UWaterloo. The code updates pheromones by using pheromones. 

Here the following details about the files
To setup the number of iteration in the code
1. Number of ants = 30 -> Pick a number of ants
2. Best ants = 5 -> Pick the range of results you want to get in the ants
3. Number of iterations = 700 -> Update to fast convergence
4. Decay = 0.9 To evaporate pheromones, the rate in which this decays
5. Alpha = 0.7 To update relevance in the pheromones received
6. Beta = 0.7 To provide more relevance to the weights were provided

To run the code on its own. At the end of the code there is a sample example.py. Copy the code and create a file example.py. Paste the code and test with the examples we are using.

`python3 example.py`

To run the experiments run the following:
`python3 runExperiments`

The following path will provide the following results:
1. The results of the random generator code. These results are updated with a png file
2. The results of the aco algorithm. These results are updated with a png file
3. The results of a comparison of each algorithm with the updates as a png file.

