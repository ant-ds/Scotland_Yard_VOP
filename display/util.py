import cv2
import math

import display.constants as dconst
import game.constants as gconst


def drawPlayers(imgdata, positions, mrx=None):
    """
    Given image data and a list of detectives' positions, draws circles indicating these
    positions using parameters defined in constants
    """
    assert(isinstance(positions, list))
    for pos in positions:
        assert(isinstance(pos, int))
    assert(mrx is None or isinstance(mrx, int))

    frac = [float(dconst.DISPLAY_SIZE[i]) / float(dconst.IMG_TOTAL_SIZE[i]) for i in range(2)]

    dimensions = tuple([math.floor(dconst.POSITION_RADIUS * dim) for dim in frac])

    for i, pos in enumerate(positions):
        position = gconst.VERTEX_POSITIONS[pos]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = dconst.PLAYER_COLORS['detectives'][i]

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
        position = gconst.VERTEX_POSITIONS[mrx]
        position = tuple(math.ceil(frac[i] * position[i]) for i in range(2))  # resized to DISPLAY_SIZE

        color = dconst.PLAYER_COLORS['mrx']

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
    img = cv2.resize(img, dconst.DISPLAY_SIZE)

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


