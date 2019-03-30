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

from game.game import ScotlandYard
from game.util import readConfig
from ai.human import misterx
import ai.ml.detective as detAI
import game.constants as const
from detectivestate import DetectiveState

from pickle import load
import numpy as np
#import tensorflow.keras as ks
from itertools import product

# Parameters
episodes = 0
timesteps = 0
coordinate_anchors = 10
gamesize = 199
det_amount = 4

# Constants
def initTrainingConstants(coordinate_anchors, gamesize, det_amount):
    config = readConfig('MLsettings.ini')
    game = ScotlandYard(cfg=config, size=gamesize, numDetectives=det_amount)
    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    game.addDetectives([detAI.AIReinforcementDetective(idNumber=i, game=game) for i in range(det_amount)])

    # load coordinates
    coord = load(open(f"Distances_A{coordinate_anchors}_s{gamesize}.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, game
longest_path, coordinates, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)   # for normalization
targetmodel = None






# 1 Initialize replay memory capacity
memory = []




# action: hier soort pseudo decide uitvoeren voor alle detectives (Q value)









print('Training is over')









def chooseAction(model, game, detstate, epsilon):
    # get all actions
    # epsilon-greedy
    # vectorize data
    # get Q values with model.predict
    # set action in detectives
    # return action

    chosen_action = None
    chosenQ = 0
    
    # possible action for each detective
    poss_det_action = [game.board.getOptions(detective, doubleAllowed = False) for detective in game.detectives]
    possible_actions = list(zip(product(*poss_det_action)))
    # filter actions with non-unique position combinations
    possible_actions = [action for action in possible_actions if len([act[0] for act in action]) == len(set([act[0] for act in action]))]
    if np.random.uniform() <= epsilon:
        chosen_action = possible_actions[np.random.randint(0, len(possible_actions) - 1)]
        chosenQ = model.predict(formalizeStateAction(detstate, [act[0] for act in chosen_action[0]], [act[1] for act in chosen_action[0]]))
    
    else:
        # bereken Q value voor elke mogelijke actie
        # maak functie die DetectiveState en actie neemt en omzet in goede vorm
        Qvalues = []
        for action in possible_actions:
            inputvec = formalizeStateAction(detstate, [ act[0] for act in action[0]], [ act[1] for act in action[0]])
            #Qvalues.append(model.predict(inputvec))
            #print(f'inputvec: {inputvec}')
            Qvalues = [i for i in range(0, len(possible_actions))]
        chosenQ = max(Qvalues)
        chosen_action = possible_actions[Qvalues.index(chosenQ)]

    for i in range(0, len(game.detectives)):
        game.detectives[i].nextaction = chosen_action[0][i]

    return chosen_action, chosenQ


# returns state action as numpy array for NN input
def formalizeStateAction(detstate, actionpos, actioncards):
    vec = []
    for i in range(0, len(detstate.detectivepos)):
        vec = vec + detstate.detectivepos[i] + detstate.detectivecards[i]
    vec.append(detstate.revealcountdown)
    vec.append(detstate.gamecountdown)

    for i in range(0, len(actionpos)):
        vec = vec + [ x / longest_path for x in coordinates[actionpos[i]] ]
        if actioncards[i] == 'taxi':
            vec = vec + [0, 0 , 1]
        else:
            if actioncards[i] == 'bus':
                vec = vec + [0, 1, 0]
            else:
                vec = vec + [1, 0, 0]


    return np.append(np.array(vec), detstate.possiblemrx)






# formalize game state, action, reward and following state
def generateMemUnitDet(game):
    memunit = []

    ## Game state
    # detectives and their transport cards
    for det in range(0, game.numDetectives):
        detposition = coordinates[det.position] / longest_path  # normalize coordinates
        memunit.append(detposition)
        memunit.append(det.cards['underground'] / 4)
        memunit.append(det.cards['bus'] / 8)
        memunit.append(det.cards['taxi'] / 11)

    
    # Reveal countdown
    revealcountdown = -1
    for i in const.MRX_OPEN_TURNS[:-1]:
        revealcountdown = i - len(game.misterx.history)
        if revealcountdown >= 0:
            break

    # Wanneer de laatste reveal geweest is,
    # wordt de teller altijd op 4 (= maximale tellerwaarde) gezet
    # zodat de detectives altijd de indruk hebben dat de reveal nog ver weg is
    # en dus moeten ze blijven jagen op mister X.
    # 4 is wordt als maximum genomen zodanig dat genormaliseerd kan worden
    if revealcountdown < 0:
        revealcountdown = 4
    memunit.append(revealcountdown / 4)

    # add countdown to end of game
    memunit.append((game.turns - len(game.misterx.history)) / game.turns)

    # Mr X possible positions
    ## TODO: posvector is een numpy array! let op met appenden aan memunit
    possiblepos = game.board.possibleMisterXPositions()
    origposvector = np.zeros(1, len(possiblepos))
    for i in range(0, len(possiblepos)):
            origposvector[possiblepos[i]] = 1



    return memunit


""" Testing """


def main():
    longest_path, coordinates, game = initTrainingConstants(10, 199, 4)

    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    # game.addMisterX(randomMrX.ExampleAIImplementationRandomMisterX(name="Random Mr. X", game=game, blackCards=4))
    game.addDetectives([detAI.AIReinforcementDetective(idNumber=i, game=game) for i in range(4)])

    game.board.assignStartPositions()
    game.running = True
    chosen_action, chosenQ = chooseAction(None, game, DetectiveState().extractDetState(game, coordinates, longest_path), 0)
    print(f'Chosen action: {chosen_action}')
    print(f'ChosenQ: {chosenQ}')
    game.update()

    detstate = DetectiveState()
    detstate.extractDetState(game, coordinates, longest_path)
    # detstate.display()


if __name__ == '__main__':
    main()