# Holds (neighbour, transport) tuple-lists on index == starting point
# Example: node 1 is connected with node 3 by a bus line => CONNECTIONS[1] = (3, 'bus')
# TODO: complete data using physical board
CONNECTIONS = [
    None,  # Index 0 probably not used by physical board?
    [(2, 'taxi'), (8, 'underground')],
    [(5, 'bus'), (5, 'underground')],
    [(2, 'taxi'),],
    [],
    [],
    [],
    [(5, 'bus'),],
    [],
    [(2, 'taxi'),],
    [],
]

EDGE_COLORS = {
    'bus': 'r',
    'taxi': 'g',
    'underground': 'b',
}
