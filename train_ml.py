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

from ai.ml.mlutils import chooseAction, formalizeStateAction, initTrainingConstants, generateMemUnitDet
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
epsilon = 0.444
learning_rate = 0.005
lr_decay = 1e-7         # rather low because model.fit will be called very often with little input
gamma = 0.99            # MDP discount parameter

target_upd_cycles = 5   # amount of NN trainings before target NN gets updated
episodes = 25
warmup_capacity = 150  # amount of memory units to generate before starting to train
batch_size = 32
training_period = 3     # amount of games to play before 1 NN training

play_test_games_interval = 25
test_games = 100
memorymax = 50000

# 1 Initialize game
longest_path, coordinates, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)

# 2 Initialize NN
layersizes = [64, 32, 16]
model = newDenseModel(305, layersizes, learning_rate, lr_decay)
NAME = f'DetDense{layersizes}_Eps{episodes}{int(time.time())}'
tensorboard = ks.callbacks.TensorBoard(log_dir=f'tensorboardlogs/{NAME}')

# 3 Clone NN = targetNN
targetNN = newDenseModel(305, layersizes, learning_rate, lr_decay)
targetNN.set_weights(model.get_weights())

# 4 Initialize replay memory capacity
memory = []
print('Warming up memory')
while(len(memory) < warmup_capacity):
    game.reset()    # = initTrainingConstants(coordinate_anchors, gamesize, det_amount)    # game.reset()  # TODO
    # game.board.assignStartPositions()

    game_done = False
    while(not game_done):
        memunit, game_done = generateMemUnitDet(model, game, epsilon, coordinates, longest_path)
        memory.append(memunit)

# 5 Training
print('Start training')
for i in range(0, episodes):
    print(f'Episode {i}')

    # play game
    for _ in range(0, training_period):

        # reset game
        game.reset()    # = initTrainingConstants(coordinate_anchors, gamesize, det_amount)    # game.reset()  # TODO
        # game.board.assignStartPositions()

        game_done = False
        while(not game_done):
            memunit, game_done = generateMemUnitDet(model, game, epsilon, coordinates, longest_path)
            memory.append(memunit)

    if len(memory) > memorymax:
        del memory[:1000]
    print('Games played')

    # sample batch and preprocess
    sam = sample(memory, batch_size)
    batch = [formalizeStateAction(s.currDetState, s.action, longest_path, coordinates) for s in sam]
    arrbatch = np.array(batch).reshape(batch_size, 305)

    print('Setting up target batch')
    target_batch = []
    for s in sam:
        _, targetQ = chooseAction(targetNN, s.nextPossActions, s.nextDetState, 0, longest_path, coordinates)
        target_batch.append(s.reward + gamma * targetQ)

    print('Optimizing on batch')
    # pass batch to NN and update weights
    print(f'Loss: {model.train_on_batch(arrbatch, np.reshape(np.array(target_batch), (batch_size, 1)))}')

    if i % target_upd_cycles == 0:
        targetNN.set_weights(model.get_weights())

    if i % 5 == 0:
        model.save(f'ai/ml/models/{NAME}')

print('Training done')
