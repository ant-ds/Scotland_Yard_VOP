import zipfile


def main():
    data = {'ai': {}, 'random': {}}
    archive = zipfile.ZipFile('history/manylayermodelFULL.zip', 'r')
    for fn in archive.namelist():
        datapart = 'ai'
        if '.hist' not in fn:
            continue
        if 'random' in fn.lower():
            datapart = 'random'
        episodes = fn.replace('episodes', '').replace('VRandom', '').split('model')[1].split('/')[0]
        if episodes not in data[datapart].keys():
            data[datapart][episodes] = {}
        fp = archive.open(fn)
        lines = fp.readlines()
        # Lines gives b'' strings, so decode from binary to string before splitting
        length = len(lines[1].decode('UTF-8').replace('::\n', '').split('::'))
        length -= len(lines[2].decode('UTF-8').replace(';\n', '').split(';'))
        status = str(int(lines[0]))  # game status code for a dict key
        if status not in data[datapart][episodes].keys():
            data[datapart][episodes][status] = []
        data[datapart][episodes][status].append(length)

    files = ['analytics/avg_game_length_AI.txt', 'analytics/avg_game_length_Random.txt']
    i = 0
    for player, player_info in data.items():
        with open(files[i], 'w') as outfile:
            for episodes, epi_info in player_info.items():
                toWrite = f"{episodes} "
                for status in range(-2, 2):
                    if str(status) not in epi_info.keys():
                        toWrite += "0 "  # not availlable
                    else:
                        lengths = epi_info[str(status)]
                        avg_length = float(sum(lengths)) / len(lengths)
                        toWrite += f"{avg_length:.4f} "
                outfile.writelines(toWrite + '\n')
        i += 1


if __name__ == '__main__':
    main()
