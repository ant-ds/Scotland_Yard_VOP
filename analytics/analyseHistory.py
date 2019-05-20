import os
import numpy as np
import zipfile


def score(arr):
    if sum(arr) > 0:
        return f"\tDetectives: {arr[0]}; ({arr[0]/sum(arr)*100:.3f}%)\n\tMrx: {arr[1]}; ({arr[1]/sum(arr)*100:.3f}%)"
    return "\tEmpty"


def printResult(foldername, arr):
    if foldername is None:  # Don't know where it comes from but it exists
        return
    base = f"{foldername}: "
    if sum(arr) > 0:
        base += f"{sum(arr)}"
    base += f'\n{score(arr)}'
    print(base)


def readFile(data, arr):
    result = data[0]
    if result >= 0:
        arr[0] += 1
    else:
        arr[1] += 1
    return arr


def readHistoryFile(fpath, arr, filepath=True):
    if filepath:
        with open(fpath, 'r') as fp:
            lines = fp.readlines()
            status = int(lines[0])
        return readFile([status], arr)
    else:
        fp = fpath
        try:
            lines = fp.readlines()
            status = int(lines[0])
        except Exception as e:
            print(fp)
            print(e)
            return arr
        return readFile([status], arr)


def readHistoryZip(filename):
    archive = zipfile.ZipFile(filename, 'r')
    d = {}
    for fn in archive.namelist():
        if '.hist' in fn:
            parts = fn.split('/')
            d[parts[0]] = readHistoryFile(archive.open(fn), d[parts[0]], filepath=False)
        else:
            d[fn.split('/')[0]] = [0, 0]
    
    for k, v in d.items():
        printResult(k, v)
    
    return [0, 0]


def readNumpyZip(filename, data):
    s = [0, 0]
    for k, v in data.items():
        s = readFile(v, s)
    return s


def main(unix: bool, basepath=None):
    if unix:
        sep = '/'
    else:
        sep = '\\'

    if basepath is None:
        basepath = os.getcwd()
        basepath = basepath.split(f'{sep}analytics')[0]
        basepath += f"{sep}history"

        name = "Main Folder"
    else:
        name = basepath.split(sep)[-1]

    r = [0, 0]

    for f in sorted(os.listdir(basepath)):
        fpath = basepath + f"{sep}" + f
        if '.' not in fpath.split(sep)[-1]:
            printResult(main(unix, basepath=fpath), r)
        elif '.hist' in fpath:
            r = readHistoryFile(fpath, r)
        else:
            if "zip" in f:
                if f.startswith('np_'):
                    data = np.load(fpath)
                    printResult(f, readNumpyZip(f, data))
                else:
                    # .hist zip file
                    printResult(f, readHistoryZip(fpath))
            else:
                data = np.load(fpath)
                r = readFile(data, r)
    printResult(name, r)


if __name__ == '__main__':
    main(True)
