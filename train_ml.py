# Training NN
# 1 Init replay memory capacity
# 2 Init game
# 3 Init NN with random weights, specify loss
# 4 Clone NN, call it the "target" network
# 5 For each episode:
#     - reset game
#     - for each time step:
#         * select action: epsilon-greedy
#         * execute action and observe Rt+1 and St+1
#         * store exp in replay memory
#         * sample random batch from memory and preprocess (prioritized exp replay?)
#         * pass batch to network
#         * calculate loss between NN Q and target Q
#         * gradient descent updates weights in NN
#         * after x time steps: update weights in target network

from ai.human import misterx
import ai.ml.detective as detAI
from ai.ml.mlutils import chooseAction, formalizeStateAction, initTrainingConstants, generateMemUnitDet
import game.constants as const
from detectivestate import DetectiveState
from ai.ml.models.densemodel import newDenseModel

import numpy as np
from random import sample
import time
import tensorflow.keras as ks

# Game parameters
coordinate_anchors = 10
gamesize = 199
det_amount = 4

# Hyperparameters
epsilon = 1
learning_rate = 0.001
gamma = 0.99            # MDP discount parameter
target_upd_cycles = 5   # amount of NN trainings before target NN gets updated
episodes = 2
warmup_capacity = 100  # amount of memory units to generate before starting to train
batch_size = 64
training_period = 4     # amount of games to play before 1 NN training



# 1 Initialize game
longest_path, coordinates, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)

# 2 Initialize NN
model = newDenseModel(305, [64, 64, 32])
NAME = f'DetDense{[64, 64, 32]}_{int(time.time())}'
tensorboard = ks.callbacks.TensorBoard(log_dir=f'tensorboardlogs/{NAME}')

# 3 Clone NN = targetNN
targetNN = newDenseModel(305, [64, 64, 32])
targetNN.set_weights(model.get_weights())

# 4 Initialize replay memory capacity
memory = []
print('Warming up memory')
while(len(memory) < warmup_capacity):
    print(f'Memory capacity: {len(memory)}')
    _, _, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)    #game.reset()  # TODO
    game.board.assignStartPositions()

    game_done = False
    while(not game_done):
         memunit, game_done = generateMemUnitDet(model, game, epsilon, coordinates, longest_path)
         memory.append(memunit)

memory[0].display()
memory[1].display()
memory[30].display()

# 5 Training
print('Start training')
for i in range(0, episodes):
    print(f'Episode {i}')
    # play game
    for _ in range(0, training_period):

        # reset game
        _, _, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)    #game.reset()  # TODO
        game.board.assignStartPositions()

        game_done = False
        while(not game_done):
            memunit, game_done = generateMemUnitDet(model, game, epsilon, coordinates, longest_path)
            memory.append(memunit)

    # sample batch and preprocess
    sam = sample(memory, batch_size)
    batch = [formalizeStateAction(s.currDetState, s.action, longest_path, coordinates) for s in sam]
    target_batch = []
    for s in sam:
        _, targetQ = chooseAction(targetNN, s.nextPossActions, s.nextDetState, 0, longest_path, coordinates)
        target_batch.append(s.reward + gamma * targetQ)

    # pass batch to NN and update weights
    model.fit(batch, target_batch, batch_size=batch_size, epochs=1, callbacks=[tensorboard], verbose=2)

    if i % target_upd_cycles == 0:
        targetNN.set_weights(model.get_weights())

    
model.save(f'ai/ml/models/{NAME}')






""" Testing """


# def main():
#     longest_path, coordinates, game = initTrainingConstants(10, 199, 4)

#     game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
#     game.addDetectives([detAI.AIReinforcementDetective(idNumber=i, game=game) for i in range(4)])

#     game.board.assignStartPositions()
#     game.running = True
#     poss_det_action = [game.board.getOptions(detective, doubleAllowed = False) for detective in game.detectives]

#     chosen_action, chosenQ = chooseAction(None, poss_det_action, DetectiveState().extractDetState(game, coordinates, longest_path), 0, longest_path, coordinates)
#     #print(f'Chosen action: {chosen_action}')
#     #print(f'ChosenQ: {chosenQ}')
#     for i in range(0, len(game.detectives)):
#         game.detectives[i].nextaction = chosen_action[i]
#     game.update()

#     detstate = DetectiveState()
#     detstate.extractDetState(game, coordinates, longest_path)
#     # detstate.display()


# if __name__ == '__main__':
#     main()