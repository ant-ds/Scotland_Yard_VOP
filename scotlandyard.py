import argparse
import time

from game.game import ScotlandYard

from ai.human import misterx, enhanceddetective

import display.gui as gui
import ai.random.misterx as randomMrX
import ai.random.detective as randomDetective
from ai.ml.mldetective import AIModelDetective
import game.util as util
from pickle import load


def main(args):
    start = time.time()
    config = util.readConfig('settings.ini')
    runs = int(args['runs'])
    episodes = int(args['episodes'])
    random_ = args['random']
    percent = runs / 100
    game = ScotlandYard(cfg=config, proj=args['proj'])

    coordinate_anchors = 14
    gamesize = 199
    coordinates = load(open(f"Distances_A{coordinate_anchors}_s{gamesize}_noferry.pickle", "rb"))

    longest_path = 0
    for co in coordinates:
        if longest_path < max(co):
            longest_path = max(co)
    
    if random_ != 'y':
        game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    else:
        game.addMisterX(randomMrX.ExampleAIImplementationRandomMisterX(name=f"Random Mr. X", game=game, blackCards=4))
    # game.addMisterX(AIModelMisterX(game=game, name="AI Mister X", longest_path=longest_path, coordinates=coordinates, modelname="ai\ml\MrXmodels\DetDense[128, 128, 64, 64, 32, 32, 16, 16]_adv_MrX_epi26160"))

#     game.addDetectives([enhanceddetective.ExampleAIImplementationDetective(idNumber=i, game=game) for i in range(4)])
    # game.addDetectives([randomDetective.ExampleAIImplementationRandomDetective(idNumber=i, game=game) for i in range(4)])

    game.addDetectives(
        [
            AIModelDetective(
                idNumber=i,
                game=game,
                longest_path=longest_path,
                coordinates=coordinates,
                modelname=f"ai/ml/models/DetDense[128, 128, 128, 64, 64, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16]_adv_Det1556643593_epi{episodes}.model") 
            for i in range(5)
        ]
    )
    
    t = time.time()
    print(f"Initialisation took {t - start} seconds.")
    
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

        if i % percent == 0:
            print(f"{int(i/percent)}%")

    stop = time.time()
    print(f"{runs} games took {stop - t} seconds, averaging {(stop - t) / runs} seconds per loop")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', default=33800)
    parser.add_argument('--random', default='n')
    parser.add_argument('--runs', default=1)
    parser.add_argument('--proj', default='')
    args = vars(parser.parse_args())
    main(args)
