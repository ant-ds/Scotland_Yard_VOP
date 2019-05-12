"""
Utilities for training procedure
"""

import numpy as np
from pickle import load

from game.util import readConfig
from game.game import ScotlandYard
from ai.human import misterx
import ai.ml.trainingdetective as detAI
from detectivestate import DetectiveState, MrXState
from ai.ml.memunitdet import MemUnitDet, MemUnitMrX
from networkx import shortest_path_length
import tensorflow as tf


# returns state action as numpy array for NN input
def formalizeStateAction(detstate, action, longest_path, coordinates):
    # add acting detective's position and cards
    # vec = [detstate.detectivepos] + detstate.detectivecards
    vec = [x / longest_path for x in coordinates[action[0] - 1]] + detstate.detectivecards   # merge 2 lists into a new one TODO FIX POSITIE

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
    # print(len(vec))

    return vec.reshape(-1, len(vec))


# returns state action as numpy array for NN input
def formalizeStateActionMrX(mrxstate, action, longest_path, coordinates):
    # add position and cards
    vec = [x / longest_path for x in coordinates[action[0] - 1]] + [mrxstate.blackcards / 4, mrxstate.doublemoves / 2]

    # add detective position
    for otherp in mrxstate.detectivepos:
        vec.extend([x / longest_path for x in coordinates[otherp - 1]])

    # add other state fields
    vec.extend(mrxstate.detectivecards)
    vec.extend([mrxstate.revealcountdown, mrxstate.gamecountdown])
    vec.extend(mrxstate.detdefeated)

    # add action position and transportation
    vec.extend([x / longest_path for x in coordinates[action[0] - 1]])
    if action[1] == 'taxi':
        vec.extend([0, 0, 0, 1])
    elif action[1] == 'bus':
        vec.extend([0, 0, 1, 0])
    elif action[1] == 'underground':
        vec.extend([0, 1, 0, 0])
    elif action[1] == 'black':
        vec.extend([1, 0, 0, 0])
    else:
        vec.extend([0, 0, 0, 0])

    vec = np.array(vec)
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


def chooseActionMrX(model, poss_actions, mrxstate, epsilon, longest_path, coordinates):
    
    chosen_action = mrxstate.position, None
    chosenQ = 0

    if not poss_actions:    # making sure chooseAction still works even if no actions are possible
        chosenQ = model.predict(formalizeStateActionMrX(mrxstate, chosen_action, longest_path, coordinates))
        return chosen_action, chosenQ

    if np.random.uniform() <= epsilon:  # exploration
        chosen_action = poss_actions[np.random.randint(0, len(poss_actions))]  # randint(): upper bound excluded
        chosenQ = model.predict(formalizeStateActionMrX(mrxstate, chosen_action, longest_path, coordinates))

    else:   # exploitation
        Qvalues = []
        for action in poss_actions:
            Qvalues.append(model.predict(formalizeStateActionMrX(mrxstate, action, longest_path, coordinates)))
        chosenQ = max(Qvalues)
        chosen_action = poss_actions[Qvalues.index(chosenQ)]

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
            if not gameover:
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


def generateMemUnitsAdv(modelDet, modelMrX, game, epsilon, coordinates, longest_path):
    exp_base = 0.9  # number by which the rewards will be multiplied going backwards through the turns
    gameover = False
    memoryDet = [[] for _ in range(len(game.detectives))]
    memoryMrX = []
    while(not gameover):
        memunits = [MemUnitDet() for _ in game.detectives]
        memunitMrX = MemUnitMrX()

        # state & action
        memunitMrX.currMrXState = MrXState().extractMrXState(game)
        game.misterx.nextaction, __ = memunitMrX.action, _ = chooseActionMrX(modelMrX, game.board.getOptions(game.misterx, doubleAllowed=False), memunitMrX.currMrXState, epsilon, longest_path, coordinates)
        for i, unit in enumerate(memunits):
            unit.currDetState = DetectiveState().extractDetState(game, i)
            game.detectives[i].nextaction, __ = unit.action, _ = chooseAction(modelDet, game.board.getOptions(game.detectives[i], doubleAllowed=False), unit.currDetState, epsilon, longest_path, coordinates)

        # reward
        gameover, statuscode = game.update()
        if gameover:
            shortest_paths = [shortest_path_length(game.board.graph, detectivepos, game.misterx.position) for detectivepos
                              in [detective.position for detective in game.detectives]]
            farthest = max(shortest_paths)
            if statuscode >= 0:
                memunitMrX.reward = -100
                for i, unit in enumerate(memunits):
                    if shortest_paths[i] != 0:
                        unit.reward = 100 / (shortest_paths[i] + 1)
                    else:
                        unit.reward = 100
            else:
                memunitMrX.reward = 100
                for i, unit in enumerate(memunits):
                    unit.reward = -100 * shortest_paths[i] / farthest

        # next state
        if not gameover:
            memunitMrX.nextMrXState = MrXState().extractMrXState(game)
            memunitMrX.nextPossActions = game.board.getOptions(game.misterx, doubleAllowed=False)
            for i, unit in enumerate(memunits):
                unit.nextDetState = DetectiveState().extractDetState(game, i)
                unit.nextPossActions = game.board.getOptions(game.detectives[i], doubleAllowed=False)

        # save the memunits for the current turn in memory
        memoryMrX.append(memunitMrX)
        for i, unit in enumerate(memunits):
            memoryDet[i].append(unit)

    # make rewards exponentially smaller going backwards through the turns
    for i in range(len(game.detectives)):
        for j in range(len(memoryDet[i]) + 1)[2:]:
            memoryDet[i][-j].reward = memoryDet[i][-j + 1].reward * exp_base
    
    for j in range(len(memoryMrX) + 1)[2:]:
        memoryMrX[-j].reward = memoryMrX[-j + 1].reward * exp_base
    
    return [unit for sublist in memoryDet for unit in sublist], memoryMrX  # flatten the list


# Constants
def initTrainingConstants(coordinate_anchors, gamesize, det_amount):

    # pas readconfig aan zodat altijd specifieke settings gebruikt worden voor de training
    config = readConfig('MLsettings.ini')
    game = ScotlandYard(cfg=config, size=gamesize, numDetectives=det_amount)
    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    game.addDetectives([detAI.AIReinforcementDetective(idNumber=i, game=game) for i in range(det_amount)])

    # load coordinates
    coord = load(open(f"Distances_A{coordinate_anchors}_s{gamesize}_noferry.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, game


def initTrainingConstantsAdv(coordinate_anchors, gamesize, det_amount):

    # pas readconfig aan zodat altijd specifieke settings gebruikt worden voor de training
    config = readConfig('MLsettings.ini')
    game = ScotlandYard(cfg=config, size=gamesize, numDetectives=det_amount)
    game.addMisterX(detAI.AITrainingMisterX(game=game, name="AI Mister X", blackCards=4))
    game.addDetectives([detAI.AIReinforcementDetective(idNumber=i, game=game) for i in range(det_amount)])

    # load coordinates
    coord = load(open(f"Distances_A{coordinate_anchors}_s{gamesize}_noferry.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, game
