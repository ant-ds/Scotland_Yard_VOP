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

from ai.ml.mlutils import chooseAction, formalizeStateAction, initTrainingConstants, generateMemUnitsDet
from ai.ml.densemodel import newDenseModel

import numpy as np
from random import sample
import time
import tensorflow.keras as ks

# Game parameters
coordinate_anchors = 10 
gamesize = 199
det_amount = 5
modelinputsize = 259    # 249 voor 4 detectives

# Hyperparameters
epsilon = 0.7
epsilon_startdecay = 300    # let agent explore first, exploitation is meaningless
epsilon_decay = 3e-5   
epsilon_min = 0.2          # 0.15 as found in an article
learning_rate = 0.001
# lr_decay = 1e-8         # rather low because model.fit will be called very often with little input
gamma = 0.90            # MDP discount parameter, this used to be 0.99

target_upd_cycles = 40   # amount of NN trainings before target NN gets updated
episodes = 200000
warmup_capacity = 800  # amount of memory units to generate before starting to train
batch_size = 128
training_period = 7     # amount of games to play before 1 NN training

play_test_games_interval = 25
test_games = 100
memorymax = 20000

# 1 Initialize game
longest_path, coordinates, game = initTrainingConstants(coordinate_anchors, gamesize, det_amount)

# 2 Initialize NN
layersizes = [128, 128, 128, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8]
model = ks.models.load_model("ai\ml\models\DetDense[128, 128, 128, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8]_solodet_1556089964")  # newDenseModel(modelinputsize, layersizes, learning_rate)
NAME = f'DetDense{layersizes}_solodet_{int(time.time())}'

# 3 Clone NN = targetNN
targetNN = newDenseModel(modelinputsize, layersizes, learning_rate)
targetNN.set_weights(model.get_weights())

# 4 Initialize replay memory capacity
memory = []
print('Warming up memory')
while(len(memory) < warmup_capacity):
    game.reset()

    memory.extend(generateMemUnitsDet(model, game, epsilon, coordinates, longest_path))

# 5 Training
print('Start training')
for i in range(0, episodes):
    print(f'Episode {i}')

    # play game
    for _ in range(0, training_period):

        # reset game
        game.reset()    

        memory.extend(generateMemUnitsDet(model, game, epsilon, coordinates, longest_path))

    if len(memory) > memorymax:
        del memory[:1000]
    print('Games played')

    # sample batch and preprocess
    sam = sample(memory, batch_size)
    batch = [formalizeStateAction(s.currDetState, s.action, longest_path, coordinates) for s in sam]
    arrbatch = np.array(batch).reshape(batch_size, modelinputsize)

    target_batch = []
    for s in sam:
        if s.reward == 0:
            _, targetQ = chooseAction(targetNN, s.nextPossActions, s.nextDetState, 0, longest_path, coordinates)
            target_batch.append(s.reward + gamma * targetQ)
        else:   # game ended, no more rewards can be earned => cumulative rewards (=Q) should be zero => targetQ = 0
            target_batch.append(s.reward)

    print('Optimizing on batch')
    # pass batch to NN and update weights
    print(f'Loss: {model.train_on_batch(arrbatch, np.reshape(np.array(target_batch), (batch_size, 1)))}')

    if i % target_upd_cycles == 0:
        print('Updating target NN')
        targetNN.set_weights(model.get_weights())

    if i % 10 == 0:
        model.save(f'ai/ml/models/{NAME}')

    if epsilon > epsilon_min and i > epsilon_startdecay:
        epsilon = epsilon - epsilon_decay

print('Training done')
