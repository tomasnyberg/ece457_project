import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualization:
    def __init__(self):
        pass

    def create_network(self, path, position, weights):
        '''
        `path`, `position`, and `weights` are of type list
        '''

        n_nodes = len(path)
        self.edges = []
        self.labels = {}
        self.color_map = []
        
        self.graph = nx.Graph()

        for i in range(n_nodes - 1):
            self.edges.append([path[i], path[i+1]])
            self.labels[(path[i], path[i+1])] = weights[i]

            self.graph.add_node(path[i], pos=position[i])
            self.color_map.append('#FA8072') if i == 0 else self.color_map.append('#02CCFE')

        self.graph.add_edges_from(self.edges)

    def visualize(self):
        img = plt.imread("campus_xl.png")
        plt.imshow(img)

        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, node_color=self.color_map, with_labels=True)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.labels)
        plt.show() 
        plt.figure()

#xd = g.graph[1][2]["weights"]

nodes =[1,5,4,3,2,1]
posisition = [(100,100), (350,400), (200,300), (750,100), (600,150)] 
cost = [10, 8, 11, 3, 25]


g = GraphVisualization()
g.create_network(nodes, posisition, cost)
g.visualize()
