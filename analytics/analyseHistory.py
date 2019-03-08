import os
import numpy as np

basepath = os.getcwd()
basepath = basepath.split('\\analytics')[0]
basepath += "\\history"

r = [0, 0]
ignorelist = ["zip"]

for f in os.listdir(basepath):
    ignore = False
    for i in ignorelist:
        if i in f:
            ignore = True
    if ignore:
        continue
    fpath = basepath + "\\" + f
    data = np.load(fpath)

    result = data[0]
    r[result] += 1

print(f"Detectives: {r[0]}; ({r[0]/sum(r)*100}%)\nMrx: {r[1]}; ({r[1]/sum(r)*100}%)")
