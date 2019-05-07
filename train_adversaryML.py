from ai.ml.mlutils import chooseAction, chooseActionMrX, formalizeStateAction, formalizeStateActionMrX, initTrainingConstantsAdv, generateMemUnitsAdv
from ai.ml.densemodel import newDenseModel

import numpy as np
from random import sample
import time
import tensorflow.keras as ks
import tensorflow as tf


# ks.backend.set_floatx('float16')
# ks.backend.set_epsilon(1e-4)

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.1
session = tf.Session(config=config)

# Game parameters
coordinate_anchors = 14 
gamesize = 199
det_amount = 5
modelinputsizeDet = 279  # 259 voor 5 det, 10 anchors    # 249 voor 4 detectives
modelinputsizeMrX = 126

# Hyperparameters Detectives
epsilon = 1
epsilon_startdecay = 100    # let agent explore first, exploitation is meaningless
epsilon_decay = 1e-4   
epsilon_min = 0.2          # 0.15 as found in an article
learning_rate = 0.001
# lr_decay = 1e-8         # rather low because model.fit will be called very often with little input
gamma = 0.85

target_upd_cycles = 40   # amount of NN trainings before target NN gets updated
episodes = 200000
warmup_capacity = 2000  # amount of memory units to generate before starting to train
batch_size = 128
training_period = 6     # amount of games to play for 1 NN training
memorymax = 10000
winpercentage_period = 100

# 1 Initialize game
longest_path, coordinates, game = initTrainingConstantsAdv(coordinate_anchors, gamesize, det_amount)

# 2 Initialize NN
# Detectives
layersizesDet = [128, 128, 128, 64, 64, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16]
modelDet = newDenseModel(modelinputsizeDet, layersizesDet, learning_rate)  # ks.models.load_model("ai\ml\models\DetDense[128, 128, 128, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8]_solodet_1556089964")
NAMEDet = f'Dense{layersizesDet}_adv_Det_gamma{gamma}_{int(time.time())}'
# Mr X
layersizesMrX = [128, 128, 128, 64, 64, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16]
modelMrX = newDenseModel(modelinputsizeMrX, layersizesMrX, learning_rate)  # ks.models.load_model("ai\ml\models\DetDense[128, 128, 128, 64, 64, 64, 32, 32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 8, 8]_solodet_1556089964")
NAMEMrX = f'Dense{layersizesMrX}_adv_MrX_gamma{gamma}_{int(time.time())}'

# 3 Clone NN = targetNN
targetNNDet = newDenseModel(modelinputsizeDet, layersizesDet, learning_rate)
targetNNDet.set_weights(modelDet.get_weights())
targetNNMrX = newDenseModel(modelinputsizeMrX, layersizesMrX, learning_rate)
targetNNMrX.set_weights(modelMrX.get_weights())

# 4 Initialize replay memory capacity
memoryDet = []
memoryMrX = []
MrXwins = 0
Detwins = 0
gamesplayed = 0
statfile = open(f"ai/ml/stats/stats_{NAMEDet}.txt", "w")
print('Warming up memory')
while(len(memoryDet) < warmup_capacity):
    game.reset()

    detMemUnits, mrxMemUnits = generateMemUnitsAdv(modelDet, modelMrX, game, epsilon, coordinates, longest_path)
    memoryDet.extend(detMemUnits)
    memoryMrX.extend(mrxMemUnits)

    gamesplayed += 1
    if detMemUnits[-1].reward > 0:
        Detwins += 1
    else:
        MrXwins += 1

# 5 Training
print('Start training')
for i in range(0, episodes):
    print(f'Episode {i}')

    # play game
    for _ in range(0, training_period):

        # reset game
        game.reset()    

        detMemUnits, mrxMemUnits = generateMemUnitsAdv(modelDet, modelMrX, game, epsilon, coordinates, longest_path)
        memoryDet.extend(detMemUnits)
        memoryMrX.extend(mrxMemUnits)

        gamesplayed += 1
        if detMemUnits[-1].reward > 0:
            Detwins += 1
        else:
            MrXwins += 1

        if len(memoryDet) > memorymax:
            del memoryDet[:1000]
        
        if len(memoryMrX) > memorymax:
            del memoryMrX[:1000]

    # Detective training
    # sample batch and preprocess
    sampleDet = sample(memoryDet, batch_size)
    batch = [formalizeStateAction(s.currDetState, s.action, longest_path, coordinates) for s in sampleDet]
    arrbatch = np.array(batch).reshape(batch_size, modelinputsizeDet)

    target_batchDet = []
    for s in sampleDet:
        if s.nextDetState is not None:
            _, targetQ = chooseAction(targetNNDet, s.nextPossActions, s.nextDetState, 0, longest_path, coordinates)
            target_batchDet.append(s.reward + gamma * targetQ)
        else:   # game ended, no more rewards can be earned => cumulative rewards (=Q) should be zero => targetQ = 0
            target_batchDet.append(s.reward)

    # pass batch to NN and update weights
    print(f'Loss for detectives: {modelDet.train_on_batch(arrbatch, np.reshape(np.array(target_batchDet), (batch_size, 1)))}')

    if i % target_upd_cycles == 0:
        print('Updating target NN')
        targetNNDet.set_weights(modelDet.get_weights())

    if i % 10 == 0:
        modelDet.save(f'ai/ml/models/{NAMEDet}.model')

    # MrX training
    # sample batch and preprocess
    sampleMrX = sample(memoryMrX, batch_size)
    batch = [formalizeStateActionMrX(s.currMrXState, s.action, longest_path, coordinates) for s in sampleMrX]
    arrbatch = np.array(batch).reshape(batch_size, modelinputsizeMrX)

    target_batchMrX = []
    for s in sampleMrX:
        if s.nextMrXState is not None:
            _, targetQ = chooseActionMrX(targetNNMrX, s.nextPossActions, s.nextMrXState, 0, longest_path, coordinates)
            target_batchMrX.append(s.reward + gamma * targetQ)
        else:   # game ended, no more rewards can be earned => cumulative rewards (=Q) should be zero => targetQ = 0
            target_batchMrX.append(s.reward)

    # pass batch to NN and update weights
    print(f'Loss for Mr X: {modelMrX.train_on_batch(arrbatch, np.reshape(np.array(target_batchMrX), (batch_size, 1)))}')

    if i % target_upd_cycles == 0:
        print('Updating target NN')
        targetNNMrX.set_weights(modelMrX.get_weights())

    if i % 10 == 0:
        modelMrX.save(f'ai/ml/MrXmodels/{NAMEMrX}.model')

    if i % winpercentage_period == 0:
        percDet = Detwins / gamesplayed * 100
        percMrX = MrXwins / gamesplayed * 100
        print(f'Detective win percentage: {percDet}\nMister X win percentage: {percMrX}\nGames played: {gamesplayed}')
        statfile.write(f'-----------\nEpisode {i}\nDetective win percentage: {percDet}\nMister X win percentage: {percMrX}\nGames played: {gamesplayed}\n')
        gamesplayed = 0
        Detwins = 0
        MrXwins = 0
        modelDet.save(f'ai/ml/models/{NAMEDet}_epi{i}.model')
        modelMrX.save(f'ai/ml/MrXmodels/{NAMEMrX}_epi{i}.model')

    if epsilon > epsilon_min and i > epsilon_startdecay:
        epsilon = epsilon - epsilon_decay

print('Training done')
statfile.close()
