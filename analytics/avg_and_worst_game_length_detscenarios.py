import zipfile


def main():
    data = {}
    archive = zipfile.ZipFile('history/schwan.zip', 'r')
    for fn in archive.namelist():
        if '.hist' not in fn:
            continue
        simulation = fn.split('/')[0]
        if simulation not in data.keys():
            data[simulation] = [0, 0, None]  # sum of lengths, amount of items added total, longest game

        fp = archive.open(fn)
        lines = fp.readlines()
        
        # Lines gives b'' strings, so decode from binary to string before splitting
        length = len(lines[1].decode('UTF-8').replace('::\n', '').split('::'))
        length -= len(lines[2].decode('UTF-8').replace(';\n', '').split(';'))
        
        data[simulation][0] += length
        data[simulation][1] += 1

        if data[simulation][2] is None or length > data[simulation][2]:
            data[simulation][2] = length

    with open('analytics/DetectiveSimulations.txt', 'w') as outfile:
        for simulation, info in data.items():
            avg_length = float(info[0]) / info[1]
            outfile.writelines(f'{simulation}: average {avg_length:.2f} turns; worst {info[2]} turns\n')


if __name__ == '__main__':
    main()
