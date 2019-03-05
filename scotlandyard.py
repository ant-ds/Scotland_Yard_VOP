import sys
import configparser

from game.game import ScotlandYard
# from ai.human import misterx
from ai.human import misterx
from ai.human import detective
import display.gui as gui

import game.util as util


from ai.human.detective import ExampleAIImplementationDetective
def main():
    app = gui.createApp(sys.argv)
    config = configparser.ConfigParser()
    config.read('settings.ini')

    if len(config.keys()) == 1:  # File doesn't exist, only default key present
        config = util.generateDefaultConfig(config)

    game = ScotlandYard(cfg=config)
    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    game.addDetectives([detective.ExampleAIImplementationDetective(game=game, name=f"Detective{i+1}") for i in range(4)])

    guiInstance = gui.createGui(game)

    if config['DISPLAY'].getboolean('multithreaded_drawing'):
        app.exec()
    else:
        game.loop()

    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
