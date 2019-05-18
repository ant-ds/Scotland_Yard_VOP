from game.constants import START_POSITIONS, CONNECTIONS


def get_dist_to_point_from_start(start, goal, skip=[]):
    "goal can be a string for transport means, or an int for a position"
    seekTransport = isinstance(goal, str)
    options = [(start, 0)]
    explored = []
    while len(options) > 0:
        newOptions = []
        for option, dist in options:
            if not seekTransport and option == goal:
                return dist
            if option in explored:
                continue
            explored.append(option)
            for transport, dests in CONNECTIONS[option].items():
                if isinstance(dests, int):
                    dests = [dests]
                if len(dests) == 0:
                    continue
                if seekTransport and transport == goal:
                    return dist
                if transport in skip:
                    continue
                
                for dest in dests:
                    newOptions.append((dest, dist + 1))
            for i, info in enumerate(CONNECTIONS):
                if i == 0:
                    continue
                for transport, dests in info.items():
                    if transport in skip:
                        continue
                    if isinstance(dests, int):
                        dests = [dests]
                    if option in dests:
                        newOptions.append((i, dist + 1))
        options = newOptions


def main():
    for pos in sorted(START_POSITIONS['mrx']):
        dist = get_dist_to_point_from_start(pos, 'underground', skip=['underground', 'ferry', 'bus'])
        print(pos, dist)


if __name__ == '__main__':
    main()
