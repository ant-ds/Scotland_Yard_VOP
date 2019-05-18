import zipfile


def convert_to_percentages(arr):
    return [float(item) / sum(arr) for item in arr]


def main():
    archive = zipfile.ZipFile('history/manylayermodelFULL.zip', 'r')
    datas = [{}, {}]
    for fn in archive.namelist():
        if '.hist' not in fn:
            continue
        if 'random' in fn.lower():
            data = datas[1]
        else:
            data = datas[0]
        episodes = fn.replace('episodes', '').replace('VRandom', '').split('model')[1].split('/')[0]
        if episodes not in data.keys():
            data[episodes] = [0 for _ in range(4)]
        fp = archive.open(fn)
        lines = fp.readlines()
        status = int(lines[0])  # game status code
        data[episodes][status + 2] += 1  # status + 2 maps -2 -> 1 to 0 -> 3
    
    files = ['analytics/status_occurencesAI.txt', 'analytics/status_occurencesRandom.txt']
    for i, data in enumerate(datas):
        with open(files[i], 'w') as fp:
            for episodes in sorted(data.keys(), key=lambda x: int(x)):
                data[episodes] = convert_to_percentages(data[episodes])
                s = f"{episodes} "
                for status in range(-2, 2):
                    s += f"{data[episodes][status]:.4f} "
                fp.writelines(s + '\n')


if __name__ == '__main__':
    main()
