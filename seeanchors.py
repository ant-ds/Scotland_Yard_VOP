import pickle
import numpy as np
anchs = pickle.load(open("Anchors10_s199.pickle", "rb"))
coordinates = pickle.load(open("Distances_A10_s199.pickle", "rb"))
print(coordinates[:10])
