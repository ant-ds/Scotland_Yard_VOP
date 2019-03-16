import cv2
import math
import numpy as np
import configparser

import display.constants as const


def getDisplaySize():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    displayMode = int(config['DISPLAY']['display_mode'])
    return const.DISPLAY_SIZE_OPTIONS[displayMode]


def drawBoard():
    img = cv2.imread('assets/board.jpg', cv2.IMREAD_COLOR)
    displaySize = getDisplaySize()
    img = cv2.resize(img, displaySize)
    return img


def drawPlayers(imgdata, positions, mrx=None):
    """
    Given image data and a list of detectives' positions, draws circles indicating these
    positions using parameters defined in constants
    """
    try:
        assert(isinstance(positions, list))
        for pos in positions:
            assert(isinstance(pos, int))
        assert(mrx is None or isinstance(mrx, int))
    except AssertionError as e:
        raise AssertionError(f"{positions}\n{mrx}\n{e}; Couldn't guarantee correct drawing with these inputs")

    displaySize = getDisplaySize()
    frac = [float(displaySize[i]) / float(const.IMG_TOTAL_SIZE[i]) for i in range(2)]

    dimensions = tuple([math.floor(const.POSITION_RADIUS * dim) for dim in frac])

    for i, pos in enumerate(positions):
        position = const.VERTEX_POSITIONS[pos]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = const.PLAYER_COLORS['detectives'][i]

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
        position = const.VERTEX_POSITIONS[mrx]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = const.PLAYER_COLORS['mrx']

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


def drawCross(imgdata, position):
    displaySize = getDisplaySize()
    frac = [float(displaySize[i]) / float(const.IMG_TOTAL_SIZE[i]) for i in range(2)]

    position = const.VERTEX_POSITIONS[position]
    position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

    dimensions = tuple([math.floor(const.POSITION_RADIUS * dim) for dim in frac])

    vertices = []
    vertexOffset = tuple([int(float(dim) / 3.0) for dim in dimensions])

    # Top left
    pos = [int(position[i] - dimensions[i]) for i in range(2)]
    vertices += [pos[0] - vertexOffset[0], pos[1] + vertexOffset[1]]
    vertices += [pos[0] + vertexOffset[0], pos[1] - vertexOffset[1]]

    # Center top
    vertices += [position[0], position[1] - vertexOffset[1]]

    # Top right
    pos = [position[0] + dimensions[0], position[1] - dimensions[1]]
    vertices += [pos[0] - vertexOffset[0], pos[1] - vertexOffset[1]]
    vertices += [pos[0] + vertexOffset[0], pos[1] + vertexOffset[1]]

    # Center right
    vertices += [position[0] + vertexOffset[0], position[1]]

    # Bottom right
    pos = [int(position[i] + dimensions[i]) for i in range(2)]
    vertices += [pos[0] + vertexOffset[0], pos[1] - vertexOffset[1]]
    vertices += [pos[0] - vertexOffset[0], pos[1] + vertexOffset[1]]

    # Center bottom
    vertices += [position[0], position[1] + vertexOffset[1]]
    
    # Bottom left
    pos = [position[0] - dimensions[0], position[1] + dimensions[1]]
    vertices += [pos[0] + vertexOffset[0], pos[1] + vertexOffset[1]]
    vertices += [pos[0] - vertexOffset[0], pos[1] - vertexOffset[1]]

    # Center left
    vertices += [position[0] - vertexOffset[0], position[1]]
    
    pts = np.array([vertices], np.int32)
    pts = pts.reshape((-1, 1, 2))

    cv2.fillPoly(
        imgdata,
        [pts],
        (0, 0, 0))
    
    return imgdata


def drawData(game):
    img = drawBoard()

    dPositions = [d.position for d in game.detectives]
    img = drawPlayers(img, dPositions, mrx=game.misterx.lastKnownPosition)

    for pos in game.board.possibleMisterXPositions():
        img = drawCross(img, pos)

    return img


def drawGame(game):
    if game.gui is not None:
        game.gui.update()
    else:
        img = drawData(game)
        cv2.imshow('Scotland Yard', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def drawReplay(dPositions, mrx=None):
    img = drawBoard()
    img = drawPlayers(img, dPositions, mrx=mrx)
    return img
