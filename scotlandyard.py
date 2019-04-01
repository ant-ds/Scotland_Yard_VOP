from game.game import ScotlandYard
import display.gui as gui
import ai.random.misterx as randomMrX
# import ai.random.detective as randomDetective
from ai.ml.mldetective import AIModelDetective
import game.util as util
from pickle import load


def main():

    config = util.readConfig('settings.ini')
    
    game = ScotlandYard(cfg=config)
    coordinate_anchors = 10
    gamesize = 199
    coordinates = load(open(f"Distances_A{coordinate_anchors}_s{gamesize}.pickle", "rb"))

    longest_path = 0
    for co in coordinates:
        if longest_path < max(co):
            longest_path = max(co)

    # game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    game.addMisterX(randomMrX.ExampleAIImplementationRandomMisterX(name=f"Random Mr. X", game=game, blackCards=4))
    # game.addDetectives([detective.ExampleAIImplementationDetective(idNumber=i, game=game) for i in range(4)])
    # game.addDetectives([randomDetective.ExampleAIImplementationRandomDetective(idNumber=i, game=game) for i in range(4)])
    game.addDetectives([AIModelDetective(idNumber=i, game=game, longest_path=longest_path, coordinates=coordinates, modelname='ai/ml/models/DetDense[64, 64, 32]_test') for i in range(4)])

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


if __name__ == '__main__':
    main()
