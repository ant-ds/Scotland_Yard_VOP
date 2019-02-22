import cv2
import game.util as util

from game.constants import DISPLAY_SIZE


def drawGame(game):
    # TODO: convert to RGB
    img = cv2.imread('board.jpg', cv2.IMREAD_COLOR)
    img = cv2.resize(img, DISPLAY_SIZE)

    dPositions = [d.position for d in game.detectives]
    img = util.drawPlayers(img, dPositions, mrx=game.misterx.position)

    # TODO: draw 'last-seen' position of Mr. X

    cv2.imshow('Scotland Yard', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
