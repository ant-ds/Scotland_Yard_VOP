"""
Utilities for training procedure
"""

import numpy as np
from pickle import load

from game.util import readConfig
from game.game import ScotlandYard
from ai.human import misterx
import ai.ml.trainingdetective as detAI
from detectivestate import DetectiveState
from ai.ml.memunitdet import MemUnitDet
from networkx import shortest_path_length


# returns state action as numpy array for NN input
def formalizeStateAction(detstate, action, longest_path, coordinates):
    # add acting detective's position and cards
    vec = [detstate.detectivepos] + detstate.detectivecards   # merge 2 lists into a new one

    # add other detective's position
    for otherp in detstate.otherpos:
        vec.extend([x / longest_path for x in coordinates[otherp - 1]])
    
    # add reveal countdown, game countdown and defeat
    vec.append(detstate.revealcountdown)
    vec.append(detstate.gamecountdown)
    vec.append(detstate.defeated)

    # add action position and transportation
    vec.extend([x / longest_path for x in coordinates[action[0] - 1]])
    if action[1] == 'taxi':
        vec.extend([0, 0, 1])
    elif action[1] == 'bus':
        vec.extend([0, 1, 0])
    elif action[1] == 'underground':
        vec.extend([1, 0, 0])
    else:
        vec.extend([0, 0, 0])

    vec = np.append(np.array(vec), detstate.possiblemrx)
    return vec.reshape(-1, len(vec))


def chooseAction(model, poss_det_action, detstate, epsilon, longest_path, coordinates):

    chosen_action = detstate.detectivepos, None
    chosenQ = 0

    if not poss_det_action:  # get Q value for state-action with defeated detective, model has to learn to avoid this situation
        chosenQ = model.predict(formalizeStateAction(detstate, chosen_action, longest_path, coordinates))
        return chosen_action, chosenQ

    if np.random.uniform() <= epsilon:  # exploration
        chosen_action = poss_det_action[np.random.randint(0, len(poss_det_action))]  # randint(): upper bound excluded
        chosenQ = model.predict(formalizeStateAction(detstate, chosen_action, longest_path, coordinates))

    else:   # exploitation
        Qvalues = []
        for action in poss_det_action:
            Qvalues.append(model.predict(formalizeStateAction(detstate, action, longest_path, coordinates)))
        chosenQ = max(Qvalues)
        chosen_action = poss_det_action[Qvalues.index(chosenQ)]  

    return chosen_action, chosenQ


# formalize game state, action, reward and following state
def generateMemUnitsDet(model, game, epsilon, coordinates, longest_path):
    exp_base = 0.9  # number by which the rewards will be multiplied going backwards through the turns
    gameover = False
    memory = [[] for _ in range(len(game.detectives))]
    while(not gameover):
        memunits = [MemUnitDet() for _ in game.detectives]

        # state & action
        for i, unit in enumerate(memunits):
            unit.currDetState = DetectiveState().extractDetState(game, i)
            game.detectives[i].nextaction, __ = unit.action, _ = chooseAction(model, game.board.getOptions(game.detectives[i], doubleAllowed=False), unit.currDetState, epsilon, longest_path, coordinates)

        # reward
        gameover, statuscode = game.update()
        if gameover:
            shortest_paths = [shortest_path_length(game.board.graph, detectivepos, game.misterx.position) for detectivepos
                              in [detective.position for detective in game.detectives]]
            farthest = max(shortest_paths)
            if statuscode >= 0:
                for i, unit in enumerate(memunits):
                    if shortest_paths[i] != 0:
                        unit.reward = 100 / (shortest_paths[i] + 1)
                    else:
                        unit.reward = 100
            else:
                for i, unit in enumerate(memunits):
                    unit.reward = -100 * shortest_paths[i] / farthest

        # next state
        for i, unit in enumerate(memunits):
            unit.nextDetState = DetectiveState().extractDetState(game, i)
            unit.nextPossActions = game.board.getOptions(game.detectives[i], doubleAllowed=False)

        # save the memunits for the current turn in memory
        for i, unit in enumerate(memunits):
            memory[i].append(unit)

    # make rewards exponentially smaller going backwards through the turns
    for i in range(len(game.detectives)):
        for j in range(len(memory[i]) + 1)[2:]:
            memory[i][-j].reward = memory[i][-j + 1].reward * exp_base
    
    return [unit for sublist in memory for unit in sublist]  # flatten the list


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
