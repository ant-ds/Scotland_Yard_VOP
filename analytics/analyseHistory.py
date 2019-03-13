import os
import numpy as np


def score(arr):
    if sum(arr) > 0:
        return f"\tDetectives: {arr[0]}; ({arr[0]/sum(arr)*100:.3f}%)\n\tMrx: {arr[1]}; ({arr[1]/sum(arr)*100:.3f}%)"
    return "\tEmpty"


def printResult(foldername, arr):
    base = f"{foldername}: "
    if sum(arr) > 0:
        base += f"{sum(arr)}"
    base += f'\n{score(arr)}'
    print(base)


def readFile(data, arr):
    result = data[0]
    arr[result] += 1
    return arr


def readZip(filename, data):
    s = [0, 0]
    for k, v in data.items():
        s = readFile(v, s)
    return s


def main(unix: bool):
    if unix:
        sep = '/'
    else:
        sep = '\\'

    basepath = os.getcwd()
    basepath = basepath.split(f'{sep}analytics')[0]
    basepath += f"{sep}history"

    r = [0, 0]

    for f in os.listdir(basepath):
        fpath = basepath + f"{sep}" + f
        data = np.load(fpath)
        if "zip" in f:
            printResult(f, readZip(f, data))
        else:
            r = readFile(data, r)
    printResult("Main folder", r)


if __name__ == '__main__':
    main(False)
