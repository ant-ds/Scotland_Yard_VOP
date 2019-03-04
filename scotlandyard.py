import sys

from game.game import ScotlandYard
import display.gui as gui

import game.util as util
import display.constants as const

from ai.human.detective import ExampleAIImplementationDetective
def main():
    app = gui.createApp(sys.argv)

    game = ScotlandYard(visualize=True, verbose=True)
    game.addDetectives([ExampleAIImplementationDetective(name=f"Detective{i+1}", game=ScotlandYard()) for i in range(4)])
    guiInstance = gui.createGui(game)

    if const.MULTITHREADED_DRAWING:
        app.exec()
    else:
        game.loop()

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
