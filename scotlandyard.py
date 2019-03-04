import sys

from game.game import ScotlandYard
from ai.human import misterx
import display.gui as gui

import game.util as util
import display.constants as const

def main():
    app = gui.createApp(sys.argv)

    game = ScotlandYard(visualize=True, verbose=True)
    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    guiInstance = gui.createGui(game)

    if const.MULTITHREADED_DRAWING:
        app.exec()
    else:
        game.loop()

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
