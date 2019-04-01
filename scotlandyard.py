import argparse

from game.game import ScotlandYard

from ai.human import misterx, enhanceddetective

import display.gui as gui
import ai.random.misterx as randomMrX
import ai.random.detective as randomDetective

import game.util as util


def main(args):
    config = util.readConfig('settings.ini')
    runs = int(args['runs'])
    game = ScotlandYard(cfg=config, proj=args['proj'])
    
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--runs', default=1)
    parser.add_argument('--proj', default='')
    args = vars(parser.parse_args())
    main(args)
