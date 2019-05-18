import zipfile
from translate import winrate


def startpos_results_per_episode(archive):
    datas = [{}, {}]
    for fn in archive.namelist():
        data = datas[0]
        if '.hist' not in fn:
            continue
        if 'random' in fn.lower():
            data = datas[1]
        episodes = fn.replace('episodes', '').replace('VRandom', '').split('model')[1].split('/')[0]
        if episodes not in data.keys():
            data[episodes] = {}
        fp = archive.open(fn)
        lines = fp.readlines()
        # Lines gives b'' strings, so decode from binary to string before splitting
        startpos = lines[1].decode('UTF-8').split(';')[0]
        status = int(lines[0])  # game status code
        if startpos not in data[episodes].keys():
            data[episodes][startpos] = [0, 0]
        if status >= 0:
            data[episodes][startpos][0] += 1
        else:
            data[episodes][startpos][1] += 1
    return datas


def startpos_results_per_simulation(archive):
    data = {}
    for fn in archive.namelist():
        if '.hist' not in fn:
            continue
        simulation = fn.split('/')[0]
        if simulation not in data.keys():
            data[simulation] = {}
        fp = archive.open(fn)
        lines = fp.readlines()
        # Lines gives b'' strings, so decode from binary to string before splitting
        startpos = lines[1].decode('UTF-8').split(';')[0]
        status = int(lines[0])  # game status code
        if startpos not in data[simulation].keys():
            data[simulation][startpos] = [0, 0]
        if status >= 0:
            data[simulation][startpos][0] += 1
        else:
            data[simulation][startpos][1] += 1
    return data


def main():
    archive = zipfile.ZipFile('history/extraDetEvaluationStartpos.zip', 'r')
    """datas = startpos_results_per_episode(archive)
    files = ['analytics/startposWinrate_full.txt', 'analytics/startposWinrateRandom_full.txt']
    for i, data in enumerate(datas):
        with open(files[i], 'w') as fp:
            for episodes in sorted(data.keys(), key=lambda x: int(x)):
                s = f"{episodes}"
                for startpos in sorted(data[episodes].keys(), key=lambda x: int(x)):
                    s += f" {winrate(data[episodes][startpos]):.4f}"
                fp.writelines(s + '\n')"""
    data = startpos_results_per_simulation(archive)
    with open('analytics/startpos_stats_simulation.txt', 'w') as outfile:
        for simulation, info in data.items():
            s = f"{simulation} "
            for startpos in sorted(data[simulation].keys(), key=lambda x: int(x)):
                s += f"{winrate(data[simulation][startpos]):.4f} "
            s += '\n'
            s.replace(" \n", "\n")  # remove trailing space
            outfile.writelines(s)


if __name__ == '__main__':
    main()
