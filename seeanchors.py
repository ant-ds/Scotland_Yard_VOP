import pickle
import numpy as np
anchs = pickle.load(open("Anchors10_s199.pickle", "rb"))
coordinates = pickle.load(open("Distances_A10_s199.pickle", "rb"))
for i in range(1, 60):
    print(f'co {i}: {coordinates[i]}')
