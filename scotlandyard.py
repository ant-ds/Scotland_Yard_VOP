import sys

from game.game import ScotlandYard

from ai.human import misterx, detective, enhanceddetective

import display.gui as gui
import ai.random.misterx as randomMrX
import ai.random.detective as randomDetective

import game.util as util


def main(runs):
    config = util.readConfig('settings.ini')
    
    game = ScotlandYard(cfg=config)    

    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    # game.addMisterX(randomMrX.ExampleAIImplementationRandomMisterX(name=f"Random Mr. X", game=game, blackCards=4))
    game.addDetectives([enhanceddetective.ExampleAIImplementationDetective(idNumber=i, game=game) for i in range(4)])
    # game.addDetectives([randomDetective.ExampleAIImplementationRandomDetective(idNumber=i, game=game) for i in range(4)])
    
    for i in range(runs):
        if config['OUTPUT'].getboolean('visualization'):
            app = gui.createApp([])
            guiInstance = gui.createGui(game)

            if config['DISPLAY'].getboolean('multithreaded_drawing'):
                app.exec()
            else:
                game.loop()

            # Please linter, use app and guiInstance somewhere
            util.clear([app, guiInstance])

        else:
            game.loop()
        game.reset()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        runs = int(sys.argv[1])
    elif len(sys.argv) == 1:
        runs = 1
    else:
        raise ValueError(f"I do not know what to do with these arguments: {sys.argv[1:]}")
    main(runs)
