def winrate(arr):
    det, mrx = arr
    return float(det) / (det + mrx)


def main():
    with open('analysisFULL.txt') as merge:
        lines = merge.readlines()

    dicts = [{}, {}]

    episodes = 0
    for line in lines:
        line = line.replace('episodes', '')  # Old artefact
        if line.startswith('manylayermodel'):
            idx = 0
            if 'VRandom' in line:
                idx = 1
                episodes = line.split('manylayermodel')[1].split('VRandom:')[0]
            else:
                episodes = line.split('manylayermodel')[1].split(':')[0]
            d = dicts[idx]
            
            if episodes not in d.keys():
                d[episodes] = [0, 0]
        elif 'Detectives' in line:
            d[episodes][0] += int(line.split(": ")[1].split(';')[0])
        elif 'Mrx' in line:
            d[episodes][1] += int(line.split(": ")[1].split(';')[0])

    outfiles = ['winrateAI_full.txt', 'winrateRandom_full.txt']
    i = 0
    for d in dicts:
        with open(outfiles[i], 'w') as outfile:
            for key in sorted(d.keys(), key=lambda x: int(x)):
                outfile.writelines(f"{key} {winrate(d[key]):.4f}\n")
        i += 1


if __name__ == '__main__':
    main()
