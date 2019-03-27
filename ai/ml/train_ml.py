# Training NN
# 1 Init replay memory capacity
# 2 Init NN with random weights, specify loss
# 3 Clone NN, call it the "target" network
# 4 For each episode:
#     - init game
#     - for each time step:
#         * select action: epsilon-greedy
#         * execute action and observe Rt+1 and St+1
#         * store exp in replay memory
#         * sample random batch from memory and preprocess (prioritized exp replay?)
#         * pass batch to network
#         * calculate loss between NN Q and target Q
#         * gradient descent updates weights in NN
#         * after x time steps: update weights in target network

from pickle import load
from game.game import ScotlandYard
from game.util import readConfig
import numpy as np

# Parameters
episodes = 0
timesteps = 0
coordinate_anchors = 9
gamesize = 107

# Constants
longest_path, coordinates, game = initTrainingConstants()   # for normalization
targetmodel = None

# 1 Initialize replay memory capacity
memory = []


print('Training is over')


# formalize game state, action, reward and following state
def prepMemUnit(game):
    memunit = []

    ## Game state
    # detectives and their transport cards
    for det in range(0, game.numDetectives):
        detposition = coordinates[det.position] / longest_path  # normalize coordinates
        for i in range(0, detposition):
                memunit.append(detposition[i])
        memunit.append(det.cards['underground'] / 4)
        memunit.append(det.cards['bus'] / 8)
        memunit.append(det.cards['taxi'] / 11)

    # Mr X possible positions
    possiblepos = game.board.possibleMisterXPositions()
    posvector = np.zeros(len(possiblepos))
    for i in range(0, len(possiblepos)):
            posvector[possiblepos[i]] = 1

        ## TODO: posvector is een numpy array! let op met appenden aan memunit

    # Reveal countdown, end of game countdown
    # TODO: wat doen we met revealcountdown na turn 18?
    revealcountdown = 
    for i in const.MRX_OPEN_TURNS:
        

    return memunit

# initialize training variables


def initTrainingConstants(coordinate_anchors, gamesize):
    config = readConfig('MLsettings.ini')

    SY = ScotlandYard(cfg=config, size=gamesize)

    # load coordinates
    coord = load(
        open(f"Distances_A{coordinate_anchors}_s{game.size}.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, SY
