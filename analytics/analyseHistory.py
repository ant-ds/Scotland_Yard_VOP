import os
import numpy as np


def score(arr):
    if sum(arr) != 0:
        return f"\tDetectives: {arr[0]}; ({arr[0]/sum(arr)*100}%)\n\tMrx: {arr[1]}; ({arr[1]/sum(arr)*100}%)\n"


def readFile(data, arr):
    result = data[0]
    arr[result] += 1
    return arr


def readZip(filename, data):
    print()
    s = [0, 0]
    for k, v in data.items():
        s = readFile(v, s)
    print(f"{filename}:\n{score(s)}")


def main():
    basepath = os.getcwd()
    basepath = basepath.split('\\analytics')[0]
    basepath += "\\history"

    r = [0, 0]

    for f in os.listdir(basepath):
        fpath = basepath + "\\" + f
        data = np.load(fpath)
        if "zip" in f:
            readZip(f, data)
        else:
            r = readFile(data, r)
    print(f"Main folder:\n{score(r)}")


if __name__ == '__main__':
    main()
