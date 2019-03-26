# Training NN
# 1 Init replay memory capacity
# 2 Init NN with random weights
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

# Parameters
episodes = 0
timesteps = 0
coordinate_anchors = 9
gamesize = 107

# Constants
longest_path, coordinates, game = initTrainingConstants()   # for normalization

# 1 Initialize replay memory capacity
memory = []



print('Training is over')






# formalize game state, action, reward and following state
def prepMemUnit(game):

    # Detectives state
    stateDet = []


# initialize training variables
def initTrainingConstants(coordinate_anchors, gamesize):
    config = readConfig('MLsettings.ini')
    
    SY = ScotlandYard(cfg=config, size=gamesize)

    # load coordinates
    coord = load(open(f"Distances_A{coordinate_anchors}_s{game.size}.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, SY
