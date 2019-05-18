from game.constants import CONNECTIONS

maxneighbours = 0
pos = 0
neighbors_of_max = []

for i, con_info in enumerate(CONNECTIONS):
    if i == 0:
        continue
    neighbours = []
    for dests in con_info.values():
        if isinstance(dests, int):
            neighbours.append(dests)
        else:
            neighbours.extend(dests)
    for j, other_con_info in enumerate(CONNECTIONS):
        if j == 0:
            continue
        for dests in other_con_info.values():
            if isinstance(dests, int):
                dests = [dests]
            if i in dests:
                neighbours.append(j)
    num_neighbours = len(list(set(neighbours)))

    if num_neighbours > maxneighbours and i not in [67, 128, 153, 46, 140]:
        maxneighbours = num_neighbours
        pos = i
        neighbors_of_max = list(set(neighbours))

print(f"Most neighbours around {pos}: {maxneighbours}::{sorted(neighbors_of_max)}")