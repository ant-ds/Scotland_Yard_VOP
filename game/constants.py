START_POSITIONS = {
    'detectives': (50, 94, 112, 103, 141, 34, 174, 53, 155, 117, 138, 123, 29, 91, 26, 13),
    'mrx': (166, 78, 127, 172, 132, 45, 106, 51, 146, 170, 35, 71, 104)
}


DISPLAY_SIZE = (800, 600)  # Size for displaying image of board on screen

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

# List with index as starting position containing dicttionaries with keys 'taxi', 'bus', 'underground' and 'ferry'
# and as value per key a tuple of connected positions via that mode of transportation
# Example: node 1 is connected with node 3 by a bus line => CONNECTIONS[1] = {'bus': (3)}
CONNECTIONS = [
    None, 
    {  # 1
        'taxi': (8, 9), 
        'bus': (58, 46), 
        'underground': (46), 
        'ferry': (), 
    }, 
    {
        'taxi': (20, 10), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (11, 12, 4), 
        'bus': (22, 23), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (13), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 5
        'taxi': (15, 16), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (7, 29), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (17), 
        'bus': (42), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (18, 19), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (19, 20), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 10
        'taxi': (11, 21, 34), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (22), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (23), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (23, 24), 
        'bus': (23, 14, 52), 
        'underground': (89, 67, 46), 
        'ferry': (), 
    }, 
    {
        'taxi': (25, 15), 
        'bus': (15), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 15
        'taxi': (26, 16, 28), 
        'bus': (41, 29), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (28, 29), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (29, 30), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (43, 31), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (32), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 20
        'taxi': (33), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (33), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (34, 23, 35), 
        'bus': (65, 34, 23), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (37), 
        'bus': (67), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (38, 37), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 25
        'taxi': (39, 38), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (27, 39), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (28, 40), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (41), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (42, 41), 
        'bus': (42, 55, 41), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 30
        'taxi': (42), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (43, 44), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (33, 45, 44), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (46), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (47, 48), 
        'bus': (46, 63), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 35
        'taxi': (36, 65, 48), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (37, 49), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (50), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (51, 50), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (52, 51), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 40
        'taxi': (41, 53, 52), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (54), 
        'bus': (52, 87), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (56, 72), 
        'bus': (72), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (57), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (58), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (46, 60, 59, 58), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (47, 61), 
        'bus': (58, 78), 
        'underground': (79, 74), 
        'ferry': (), 
    }, 
    {
        'taxi': (62), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (63, 62), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (50, 66), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 50
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (52, 68, 67), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (69), 
        'bus': (86, 67), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (54, 69), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (55, 70), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 55
        'taxi': (71), 
        'bus': (89), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (91), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (58, 73), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (59, 74), 
        'bus': (74, 77), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (76, 75), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 60
        'taxi': (61, 76), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (62, 78, 76), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (79), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (64, 80, 79), 
        'bus': (65, 100, 79), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (81, 65), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (66, 82), 
        'bus': (82, 67), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (67, 82), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (68, 84), 
        'bus': (102, 82), 
        'underground': (89, 111, 79), 
        'ferry': (), 
    }, 
    {
        'taxi': (69, 85), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (86), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 70
        'taxi': (71, 87), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (72, 89), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (90, 91), 
        'bus': (107, 105), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (74, 92), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (75, 92), 
        'bus': (94), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 75
        'taxi': (94), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (77), 
        'bus': (77), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (78, 95, 96), 
        'bus': (78, 94, 124), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (79, 97), 
        'bus': (79), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (98), 
        'bus': (), 
        'underground': (93, 111), 
        'ferry': (), 
    },  
    {  # 80
        'taxi': (100, 99), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (100, 82), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (101), 
        'bus': (100, 140), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (101, 102), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (85), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 85
        'taxi': (103), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (103, 104), 
        'bus': (102, 87, 116), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (88), 
        'bus': (105), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (89, 117), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (105), 
        'bus': (105), 
        'underground': (128, 140), 
        'ferry': (), 
    }, 
    {  # 90
        'taxi': (91, 105), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (107, 105), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (93), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (94), 
        'bus': (94), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (95), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 95
        'taxi': (122), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (97, 109), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (109, 98), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (99, 110), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (110, 112), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 100
        'taxi': (101, 113, 112), 
        'bus': (111), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (114), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (103, 115), 
        'bus': (127), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (116), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (106, 108), 
        'bus': (107, 108), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (107), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (119), 
        'bus': (161), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (117, 119), 
        'bus': (135, 116), 
        'underground': (), 
        'ferry': (115), 
    }, 
    {
        'taxi': (110, 124), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 110
        'taxi': (111), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (112, 124), 
        'bus': (124), 
        'underground': (153, 163), 
        'ferry': (), 
    }, 
    {
        'taxi': (125), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (114, 125), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (126, 132, 131, 115), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 115
        'taxi': (127, 126), 
        'bus': (), 
        'underground': (), 
        'ferry': (157), 
    }, 
    {
        'taxi': (127, 117, 118), 
        'bus': (127, 142), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (129), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (129, 134, 142), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (136), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {  # 120
        'taxi': (121, 144), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (122, 145), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (146, 123), 
        'bus': (123, 144), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (124, 137, 148, 149), 
        'bus': (124, 165, 144), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (130, 138), 
        'bus': (153), 
        'underground': (), 
        'ferry': (), 
    },  
    {  # 125
        'taxi': (131), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (127, 140), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (133, 134), 
        'bus': (133), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (142, 143, 160, 188, 172), 
        'bus': (142, 135, 161, 199, 187), 
        'underground': (140, 185), 
        'ferry': (), 
    }, 
    {
        'taxi': (135, 142, 143), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (139, 131), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (140), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (141, 140), 
        'bus': (140, 157), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (141, 142), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (136, 161, 143), 
        'bus': (161), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (162), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (147), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (152, 150), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (140, 154, 153), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 140
        'taxi': (154, 156), 
        'bus': (154, 156), 
        'underground': (153), 
        'ferry': (), 
    }, 
    {
        'taxi': (142, 158), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (143, 158), 
        'bus': (157), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (160), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (145, 177), 
        'bus': (163), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (146), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (147, 163), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (164), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (149, 164), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (150, 165), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 150
        'taxi': (151), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (152, 165, 166), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (153), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (166, 154, 167), 
        'bus': (154, 184, 180), 
        'underground': (163, 185), 
        'ferry': (), 
    }, 
    {
        'taxi': (155), 
        'bus': (156), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (156, 167, 168), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (169, 157), 
        'bus': (157, 184), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (170, 158), 
        'bus': (185), 
        'underground': (), 
        'ferry': (194), 
    }, 
    {
        'taxi': (159), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (172, 198, 186, 170), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (161, 173), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (174), 
        'bus': (199), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (175), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (177), 
        'bus': (176, 191), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (178, 179), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (179, 180), 
        'bus': (191, 180), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (183, 181), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (168, 183), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (184), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (184), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 170
        'taxi': (185), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (173, 175, 199), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (187), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (174, 188), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (175), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (177, 189), 
        'bus': (190), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (189, 191), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (191), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 180
        'taxi': (181, 193), 
        'bus': (190, 184), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (182, 193), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (195, 183), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (196), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (185, 196, 197), 
        'bus': (185), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (186), 
        'bus': (187), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (198), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (198, 188), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (199), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (190), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {  # 190
        'taxi': (191, 192), 
        'bus': (191), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (192), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (194), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    },  
    {
        'taxi': (194), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (195), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (197), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (197), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (199), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
    {
        'taxi': (), 
        'bus': (), 
        'underground': (), 
        'ferry': (), 
    }, 
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
    (209, 1126), 
    (389, 1090), 
    (479, 1069), 
    (915, 1124), 
    (988, 1100), 
    (1116, 2389), 
    (1238, 1072), 
    (1436, 1137),  # 100
    (1635, 1065), 
    (1895, 966), 
    (2062, 940), 
    (2232, 1022), 
    (2697, 1059), 
    (2874, 1085), 
    (3007, 1089), 
    (2655, 1261), 
    (1038, 1278), 
    (1184, 1146),  # 110
    (1271, 1240), 
    (1323, 1209), 
    (1523, 1221), 
    (1663, 1171), 
    (1891, 1102), 
    (2233, 1223), 
    (2471, 1312), 
    (2236, 1360), 
    (2947, 1405),  # 120
    (190, 1489), 
    (294, 1492), 
    (436, 1484), 
    (800, 1477), 
    (1008, 1431), 
    (1391, 1307), 
    (1760, 1245), 
    (2031, 1308), 
    (2377, 1709), 
    (2451, 1390), 
    (1325, 1446),  # 130
    (1439, 1370), 
    (1672, 1363), 
    (1925, 1486), 
    (2107, 1425), 
    (2451, 1471), 
    (2878, 1603), 
    (672, 1598), 
    (1072, 1518), 
    (1312, 1531), 
    (1665, 1503),  # 140
    (1995, 1531), 
    (2233, 1580), 
    (2453, 1549), 
    (226, 1744), 
    (325, 1732), 
    (467, 1724), 
    (569, 1699), 
    (718, 1677), 
    (841, 1660), 
    (981, 1608),  # 150
    (1048, 1680), 
    (1149, 1610), 
    (1202, 1692), 
    (1452, 1638), 
    (1534, 1745), 
    (1698, 1745), 
    (1844, 1759), 
    (2075, 1660), 
    (2084, 1985), 
    (2550, 1749),  # 160
    (2742, 1727), 
    (3014, 1734), 
    (454, 1801), 
    (600, 1799), 
    (874, 1846), 
    (1163, 1782), 
    (1389, 1828), 
    (1473, 1890), 
    (1694, 1861), 
    (1821, 1881),  # 170
    (2686, 2188), 
    (2300, 1864), 
    (2600, 1957), 
    (2848, 1880), 
    (2982, 1988), 
    (179, 1945), 
    (299, 1916), 
    (516, 1900), 
    (769, 1926), 
    (924, 1963),  # 180
    (1090, 1918), 
    (1171, 1938), 
    (1323, 1873), 
    (1608, 1988), 
    (1776, 2107), 
    (1956, 2065), 
    (2226, 2000), 
    (2491, 2005), 
    (305, 2116), 
    (430, 2191),  # 190
    (601, 2052), 
    (641, 2226), 
    (1040, 2071), 
    (1085, 2127), 
    (1209, 2122), 
    (1385, 2029), 
    (1409, 2149), 
    (2079, 2250), 
    (2521, 2230),  # 199
]
