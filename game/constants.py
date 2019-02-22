DISPLAY_SIZE = (800, 600)  # Size for displaying image of board on screen

IMG_TOTAL_SIZE = (3152, 2389)  # Full-scale pixel size
POSITION_RADIUS = 23  # Pixels radius of a tile on full-scale image


EDGE_COLORS = {  # TODO: could be removed
    'bus': 'r',
    'taxi': 'g',
    'underground': 'b',
}

PLAYER_COLORS = {
    'detectives': [
        (200, 0, 0),
        (0, 200, 0), 
        (0, 0, 200),
        (200, 200, 0),
        (0, 200, 200),
    ],
    'mrx': (0, 0, 0)
}

# Holds (neighbour, transport) tuple-lists on index == starting point
# Example: node 1 is connected with node 3 by a bus line => CONNECTIONS[1] = (3, 'bus')
# TODO: complete data using physical board (199 nodes) -> convention: first taxi, then bus, then underground
CONNECTIONS = [
    None,  # Index 0 probably not used by physical board?
    [(8, 'taxi'), (9, 'taxi'), (58, 'bus'), (46, 'bus'), (46, 'underground')],
    [(20, 'taxi'), (10, 'taxi')],
    [(11, 'taxi'), (12, 'taxi'), (4, 'taxi'), (22, 'bus'), (23, 'bus')],
    [(13, 'taxi')],  # node (3,'taxi') already defined in CONNECTIONS[3]
    [(15, 'taxi'), (16, 'taxi')],  # 5
    [(29, 'taxi'), (7, 'taxi')],
    [(17, 'taxi'), (42, 'bus')],
    [(18, 'taxi'), (19, 'taxi')],
    [(20, 'taxi'), (19, 'taxi')],
    [(11, 'taxi'), (21, 'taxi'), (34, 'taxi')],  # 10
    [(22, 'taxi')],
    [(23, 'taxi')],
    [(23, 'taxi'), (24, 'taxi'), (23, 'bus'), (14, 'bus'), (25, 'bus'), (46, 'underground'), (67, 'underground'), (89, 'underground')],
    [(25, 'taxi'), (15, 'taxi'), (15, 'bus')],
    [(16, 'taxi'), (26, 'taxi'), (28, 'taxi'), (41, 'bus'), (29, 'bus')],  # 15
    [(28, 'taxi'), (29, 'taxi')],
    [(29, 'taxi'), (30, 'taxi')],
    [(43, 'taxi'), (31, 'taxi')],
    [(32, 'taxi')],
    [(33, 'taxi')],  # 20
    [(33, 'taxi')],
    # [], #continue here ( node 22)
    # [],
    # [],
    # [], #25
    # [],
    # [],
    # [],
    # [],
    # [], #30
    # [],
    # [],
    # [],
    # [],
    # [], #35
    # [],
    # [],
    # [],
    # [],
    # [], #40
    # [],
    # [],
    # [],
    # [],
    # [], #45
    # [],
    # [],
    # [],
    # [],
    # [], #50
]

# Every integer defining a position on the board is index-linked with coordinates on an image of the board
VERTEX_POSITIONS = [
    None,
    (466, 177),  # 1
    (1000, 135),
    (1346, 138),
    (1558, 125),
    (2392, 158),
    (2652, 159),
    (2905, 175),
    (346, 303),
    (565, 308),
    (1174, 288),  # 10
    (1334, 314),
    (1465, 287),
    (1708, 279),
    (1956, 230),
    (2206, 209),
    (2444, 300),
    (2888, 377),
    (228, 399),
    (434, 419),
    (679, 358),  # 20
    (934, 461),
    (1344, 499),
    (1542, 393),
    (1851, 407),
    (1989, 444),
    (2185, 292),
    (2222, 413),
    (2310, 368),
    (2650, 439),
    (2976, 424),  # 30
    (316, 489),
    (609, 560),
    (822, 522),
    (1191, 560),
    (1409, 612),
    (1497, 625),
    (1626, 507),
    (1917, 518),
    (2048, 497),
    (2277, 595),  # 40
    (2374, 553),
    (2897, 556),
    (176, 598),
    (470, 658),
    (682, 692),
    (861, 638),
    (1000, 597),
    (1230, 704),
    (1573, 707),
    (1711, 622),  # 50
    (1998, 650),
    (2141, 611),
    (2300, 702),
    (2410, 667),
    (2661, 663),
    (2993, 693),
    (274, 710),
    (555, 743),
    (610, 808),
    (721, 792),  # 60
    (910, 820),
    (1012, 787),
    (1259, 912),
    (1404, 885),
    (1557, 855),
    (1647, 832),
    (1818, 804),
    (2018, 762),
    (2202, 750),
    (2418, 784),  # 70
    (2631, 787),
    (2841, 808),
    (273, 826),
    (367, 940),
    (510, 900),
    (687, 897),
    (802, 996),
    (955, 970),
    (1059, 949),
    (1297, 999),  # 80
    (1512, 1033),
    (1594, 981),
    (1785, 949),
    (1917, 891),
    (2028, 850),
    (2228, 924),
    (2438, 979),
    (2535, 997),
    (2613, 927),
    (2756, 928),  # 90
    (2961, 936),
    (194, 1048),
]
