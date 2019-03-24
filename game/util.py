import networkx as nx
import configparser

import game.constants as const


def createGraph(size):
    graph = nx.MultiGraph()

    graph.add_nodes_from(range(1, size + 1))  # size+1: Assuming 0 is not used on the physical board

    try:
        assert(len(const.CONNECTIONS) == size + 1)  # size+1: Assuming 0 is not used on the physical board
    except AssertionError:
        raise AssertionError(f"Wrong size variable: {len(const.CONNECTIONS)} != {size + 1}")

    for i in range(1, size + 1):
        # CONNECTIONS[i] contains dict with keys transport and values tuples of connections
        for transport, neighbours in const.CONNECTIONS[i].items():
            if isinstance(neighbours, int):
                # Tuple with one element is interpreted as regular int
                neighbours = [neighbours]
            for neighbour in neighbours:
                graph.add_edge(i, neighbour, transport=transport)  # If edges connect nodes not in the graph, nodes added automatically
    return graph


def isOption(options, tup):
    if tup in options:
        return True
    
    for option in options:
        if option[0] == 'double':  # for double moves, check if move is one of the two internal options
            hits = 0
            for t in tup[1:]:
                if isOption(option[1:], t):  # use recursive call to check more easily for 'black' transport calls
                    hits += 1
            if hits == len(tup[1:]):
                return True
        
        if tup == (option[0], 'black'):  # black is a valid transportation as long as the destination is reachable
            return True

    return False


def clear(items):
    """Utility function to clear data stored in a variable whose only purpose is to exist,
    f.i. PyQt5 app instances"""
    for i in range(len(items)):
        items[i] = None


def generateDefaultConfig(config, path='settings.ini'):
    config['DISPLAY'] = {
        'multithreaded_drawing': 'true',
        'display_mode': -1,
    }
    config['OUTPUT'] = {
        'verbose': 'true',
        'visualization': 'true',
    }
    config['OS'] = {
        'unix': 'false',
    }
    
    with open(path, 'w') as configfile:
        config.write(configfile)
    
    return config


def readConfig(path='settings.ini'):
    # Read configuration file
    config = configparser.ConfigParser()
    config.read('settings.ini')

    if len(config.keys()) == 1:  # Settings file doesn't exist because only default key present
        config = generateDefaultConfig(config)
    return config


class ScotlandYardException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
