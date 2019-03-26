import pickle
import numpy as np
anchs = pickle.load(open("Anchors10_s199.pickle", "rb"))
print(np.sort(anchs))
