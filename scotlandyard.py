import sys

from game.game import ScotlandYard
import display.gui as gui

import game.util as util


def main():
    app = gui.createApp(sys.argv)

    game = ScotlandYard(visualize=True, verbose=True)
    guiInstance = gui.createGui(game)

    app.exec()

    # save game data
    pass

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
