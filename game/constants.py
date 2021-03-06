START_POSITIONS = {
    'detectives': (50, 94, 112, 103, 141, 34, 174, 53, 155, 117, 138, 123, 29, 91, 26, 13), 
    'mrx': (166, 78, 127, 172, 132, 45, 106, 51, 146, 170, 35, 71, 104)
}

MRX_OPEN_TURNS = [3, 8, 13, 18, 24]

GAME_END_MESSAGES = [
    "A detective has reached Mr. X's position", 
    "Mr.x has no options left because he is surrounded", 
    "Mister X survived a full game",
    "No detective is able to move", 
]

METRO_STATIONS = [1, 13, 46, 67, 74, 79, 89, 93, 111, 128, 140, 153, 163, 165]

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
        'underground': (89, 140, 185), 
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
