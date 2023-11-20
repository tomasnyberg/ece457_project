import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualization:
    def __init__(self):
        pass

    def create_network(self, path, weights):
        '''
        `path` and `weights` are of type list
        '''
        self.edges = []
        self.labels = {}
        self.color_map = []
        for i in range(len(path) - 1):
            self.edges.append([path[i], path[i+1]])
            self.labels[(path[i], path[i+1])] = weights[i]
            self.color_map.append('#FA8072') if i == 0 else self.color_map.append('#02CCFE')
  
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.edges)

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        plt.figure()
        nx.draw(self.graph, pos, node_color=self.color_map, with_labels=True)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.labels)
        plt.axis('off')
        #plt.text(0, 0, "Cost: ")
        plt.show() 

#xd = g.graph[1][2]["weights"]

# Example usage:
# g = GraphVisualization()
# g.create_network([1,5,4,3,2,1], [10, 8, 11, 3, 25])
# #g.create_network([1,5,10,1], [10,4,2])
# g.visualize()
