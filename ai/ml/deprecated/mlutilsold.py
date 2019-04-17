"""
Utilities for training procedure
"""

from itertools import product
import numpy as np
from pickle import load

from game.util import readConfig
from game.game import ScotlandYard
from ai.human import misterx
import ai.ml.trainingdetective as detAI
from detectivestate import DetectiveState
from memunitdet import MemUnitDet


# returns state action as numpy array for NN input
def formalizeStateAction(detstate, action, longest_path, coordinates):
    vec = []
    for i in range(0, len(detstate.detectivepos)):
        vec = vec + [x / longest_path for x in coordinates[detstate.detectivepos[i] - 1]] + detstate.detectivecards[i]
    vec.append(detstate.revealcountdown)
    vec.append(detstate.gamecountdown)

    actionpos = [act[0] for act in action]
    actioncards = [act[1] for act in action]
    for i in range(0, len(actionpos)):
        vec = vec + [x / longest_path for x in coordinates[actionpos[i] - 1]]
        if actioncards[i] == 'taxi':
            vec = vec + [0, 0, 1]
        elif actioncards[i] == 'bus':
            vec = vec + [0, 1, 0]
        elif actioncards[i] == 'underground':
            vec = vec + [1, 0, 0]
        else:
            vec = vec + [0, 0, 0]

    vec = np.append(np.array(vec), detstate.possiblemrx)

    return vec.reshape(-1, len(vec))


def chooseAction(model, poss_det_action, detstate, epsilon, longest_path, coordinates):
    # get all actions
    # epsilon-greedy
    # vectorize data
    # get Q values with model.predict
    # set action in detectives
    # return action

    chosen_action = None
    chosenQ = 0

    for i, actions in enumerate(poss_det_action):
        if len(actions) == 0:
            poss_det_action[i] = [(detstate.detectivepos[i], None)]

    # possible action for each detective
    possible_actions = list(zip(product(*poss_det_action)))
    # filter actions with non-unique position combinations
    possible_actions = [action for action in possible_actions if len([act[0] for act in action[0]]) == len(set([act[0] for act in action[0]]))]
    if not possible_actions:
        return (None, None), 0
    if np.random.uniform() <= epsilon:  # exploration
        if len(possible_actions) > 1:
            chosen_action = possible_actions[np.random.randint(0, len(possible_actions) - 1)]
        else:
            chosen_action = possible_actions[0]
        chosenQ = model.predict(formalizeStateAction(detstate, chosen_action[0], longest_path, coordinates))

    else:   # exploitation
        # bereken Q value voor elke mogelijke actie
        Qvalues = []
        for action in possible_actions:
            inputvec = formalizeStateAction(detstate, action[0], longest_path, coordinates)
            Qvalues.append(model.predict(inputvec))
            # print(f'inputvec: {len(inputvec)}')
            # Qvalues = [i for i in range(0, len(possible_actions))]
        chosenQ = max(Qvalues)
        chosen_action = possible_actions[Qvalues.index(chosenQ)]  

    return chosen_action[0], chosenQ


# formalize game state, action, reward and following state
def generateMemUnitDet(model, game, epsilon, coordinates, longest_path):
    memunit = MemUnitDet()

    # state
    memunit.currDetState = DetectiveState().extractDetState(game, coordinates, longest_path)

    # action
    poss_det_action = [game.board.getOptions(detective, doubleAllowed=False) for detective in game.detectives]
    memunit.action, _ = chooseAction(model, poss_det_action, memunit.currDetState, epsilon, longest_path, coordinates)
    for i in range(0, len(game.detectives)):
        game.detectives[i].nextaction = memunit.action[i]

    # reward
    memunit.reward = 0
    gameover, statuscode = game.update()
    if gameover:
        if statuscode >= 0:
            memunit.reward = 100
        else:
            memunit.reward = -100

    # next state
    memunit.nextDetState = DetectiveState().extractDetState(game, coordinates, longest_path)

    # next possible actions
    memunit.nextPossActions = [game.board.getOptions(detective, doubleAllowed=False) for detective in game.detectives]

    return memunit, gameover

    # Constants


def initTrainingConstants(coordinate_anchors, gamesize, det_amount):

    # pas readconfig aan zodat altijd specifieke settings gebruikt worden voor de training
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
