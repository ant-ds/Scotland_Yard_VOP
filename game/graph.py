import networkx as nx
import matplotlib.pyplot as plt

from game.constants import CONNECTIONS, EDGE_COLORS


def createGraph(size):
    graph = nx.MultiGraph()

    graph.add_nodes_from(range(1, size + 1))  # size+1: Assuming 0 is not used on the physical board

    assert(len(CONNECTIONS) == size + 1)  # size+1: Assuming 0 is not used on the physical board

    for i in range(1, size + 1):
        # CONNECTIONS[i] contains list op tuples (neighbour, transport)
        for neighbour, transport in CONNECTIONS[i]:
                graph.add_edge(i, neighbour, transport=transport)  # If edges connect nodes not in the graph, nodes added automatically
    return graph
    
def drawGraph(graph):
    
    edge_color = [EDGE_COLORS[edge[2]['transport']] for edge in graph.edges(data=True)]

    nx.draw(graph, with_labels=True, node_color='grey', alpha=.5, edge_color=edge_color)
    plt.show()

#returns a list of neighboring nodes
def getOptions(graph,node):
        listret = []
        i = 0
        for n in graph.neighbors(node):
                listret.append(n)
                i+= 1
        return listret
