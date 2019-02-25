import math
import networkx as nx
import matplotlib.pyplot as plt
import cv2

from game.constants import CONNECTIONS, EDGE_COLORS
from game.constants import DISPLAY_SIZE, IMG_TOTAL_SIZE, POSITION_RADIUS, PLAYER_COLORS, VERTEX_POSITIONS


def createGraph(size):
    graph = nx.MultiGraph()

    graph.add_nodes_from(range(1, size + 1))  # size+1: Assuming 0 is not used on the physical board

    try:
        assert(len(CONNECTIONS) == size + 1)  # size+1: Assuming 0 is not used on the physical board
    except AssertionError:
        raise AssertionError(f"Wrong size variable: {len(CONNECTIONS)} != {size + 1}")

    for i in range(1, size + 1):
        # CONNECTIONS[i] contains dict with keys transport and values tuples of connections
        for transport, neighbours in CONNECTIONS[i].items():
            if isinstance(neighbours, int):
                # Tuple with one element is interpreted as regular int
                neighbours = [neighbours]
            for neighbour in neighbours:
                graph.add_edge(i, neighbour, transport=transport)  # If edges connect nodes not in the graph, nodes added automatically
    return graph

  
def drawGraph(graph):  # TODO: probably not used any longer
    edge_color = [EDGE_COLORS[edge[2]['transport']] for edge in graph.edges(data=True)]

    nx.draw(graph, with_labels=True, node_color='grey', alpha=.5, edge_color=edge_color)
    plt.show()


def drawPlayers(imgdata, positions, mrx=None):
    """
    Given image data and a list of detectives' positions, draws circles indicating these
    positions using parameters defined in constants
    """
    assert(isinstance(positions, list))
    for pos in positions:
        assert(isinstance(pos, int))
    assert(mrx is None or isinstance(mrx, int))

    frac = [float(DISPLAY_SIZE[i]) / float(IMG_TOTAL_SIZE[i]) for i in range(2)]

    dimensions = tuple([math.floor(POSITION_RADIUS * dim) for dim in frac])

    for i, pos in enumerate(positions):
        position = VERTEX_POSITIONS[pos]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = PLAYER_COLORS['detectives'][i]

        cv2.ellipse(
            imgdata, 
            position,
            dimensions,
            0,
            0,
            360,
            color,
            thickness=cv2.FILLED
        )

    if mrx is not None:
        position = VERTEX_POSITIONS[mrx]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = PLAYER_COLORS['mrx']

        cv2.ellipse(
            imgdata, 
            position,
            dimensions,
            0,
            0,
            360,
            color,
            thickness=cv2.FILLED
        )

    return imgdata
