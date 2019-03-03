import sys

from game.game import ScotlandYard
import display.gui as gui

import game.constants as const
import game.util as util


def main():
    app = gui.createApp(sys.argv)

    game = ScotlandYard(visualize=True, verbose=True)
    guiInstance = gui.createGui(game)

    stop = False
    while not stop:
        stop, status = game.update()
        pass  # Visualization function calls could be added here
    
    print(f"Game ended with status {status}::  {const.GAME_END_MESSAGES[status]}")

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
