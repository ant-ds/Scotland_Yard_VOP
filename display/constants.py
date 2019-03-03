DISPLAY_SIZE = (800, 600)  # Size for displaying image of board on screen
REFRESH_RATE = 500  # Refresh delay in ms

IMG_TOTAL_SIZE = (3152, 2389)  # Full-scale pixel size
POSITION_RADIUS = 23  # Pixels radius of a tile on full-scale image


EDGE_COLORS = {  # TODO: could be removed if graph not needed anymore
    'bus': 'r', 
    'taxi': 'g', 
    'underground': 'b', 
    'ferry': 'black', 
}

PLAYER_COLORS = {
    'detectives': [  # no (0, 200, 0), because bad visibility
        (200, 0, 0),
        (0, 0, 200),
        (200, 0, 200), 
        (0, 200, 200),
        (200, 200, 200),
    ], 
    'mrx': (0, 0, 0)
}
