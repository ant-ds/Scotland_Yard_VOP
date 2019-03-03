import cv2
import math

import display.constants as const


def getDisplaySize():
    displayMode = const.DISPLAY_MODE
    return const.DISPLAY_SIZE_OPTIONS[displayMode]


def drawPlayers(imgdata, positions, mrx=None):
    """
    Given image data and a list of detectives' positions, draws circles indicating these
    positions using parameters defined in constants
    """
    assert(isinstance(positions, list))
    for pos in positions:
        assert(isinstance(pos, int))
    assert(mrx is None or isinstance(mrx, int))

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


def drawData(game):
    img = cv2.imread('board.jpg', cv2.IMREAD_COLOR)

    displaySize = getDisplaySize()
    img = cv2.resize(img, displaySize)

    dPositions = [d.position for d in game.detectives]
    img = drawPlayers(img, dPositions, mrx=game.misterx.lastKnownPosition)

    return img


def drawGame(game):
    img = drawData(game)

    if game.gui is not None:
        game.gui.update()
    else:
        cv2.imshow('Scotland Yard', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


