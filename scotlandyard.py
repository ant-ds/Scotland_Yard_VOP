import sys
import configparser

from game.game import ScotlandYard
from ai.human import misterx
import display.gui as gui

import game.util as util


def main():
    app = gui.createApp(sys.argv)
    config = configparser.ConfigParser()
    config.read('settings.ini')

    if len(config.keys()) == 1:  # File doesn't exist, only default key present
        config = util.generateDefaultConfig(config)

    game = ScotlandYard(cfg=config)
    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    guiInstance = gui.createGui(game)

    if config['DISPLAY'].getboolean('multithreaded_drawing'):
        app.exec()
    else:
        game.loop()

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
