#  Script om knopen te zoeken die kunnen dienen als oorsprong
#  in een coordinatensysteem
# 
#  Pseudo om systeem te vinden met N oorsprongen:
#  
#   1. probeer elk paar van N knopen
#   2. bereken voor alle knopen de kortste afstand tot elke oorsprong in het gekozen paar
#   3. kijk of elke coordinaat uniek is

#   metrolijnen er uit laten?

import networkx as nx
import pickle
from game.util import createGraph

debug = 0
size = 107
gamegraph = createGraph(size)
if nx.is_connected(gamegraph) == False:
    raise "Not connected"

print(f'Searching configuration with 5 anchors for size {size}')

anchorsfound = False
for i in range(1, size - 3):
    print(f'starting i loop with index {i}')

    for j in range(i + 1, size - 2):
        print(f'starting j loop with index {j}')
        
        for k in range(j + 1, size - 1):

            for m in range(k + 1, size):

                for n in range(m + 1, size + 1):

                    node_i = i
                    node_j = j
                    node_k = k
                    node_m = m
                    node_n = n
                    alldistances = []
                    for l in range(1, size + 1):
                        nodedistance = []
                        try:
                            nodedistance.append(nx.shortest_path_length(gamegraph, l, node_i))
                            nodedistance.append(nx.shortest_path_length(gamegraph, l, node_j))
                            nodedistance.append(nx.shortest_path_length(gamegraph, l, node_k))
                            nodedistance.append(nx.shortest_path_length(gamegraph, l, node_m))
                            nodedistance.append(nx.shortest_path_length(gamegraph, l, node_n))


                        except:
                            print(f'NX: no shortest path for [{node_i}, {node_j}, {node_k}]')
                            continue

                        no_duplicate = True
                        for distance in alldistances:
                            if nodedistance[0] == distance[0] and nodedistance[1] == distance[1] and nodedistance[2] == distance[2] and nodedistance[3] == distance[3] and nodedistance[4] == distance[4]:
                                # er is een duplicaat gevonden van een bestaande node
                                if debug == 1:
                                    print(f'Duplicate found i: {i}, j: {j}, k: {k}, m: {m}, n: {n} comparing {distance} to {nodedistance} for l: {l}')
                                no_duplicate = False
                                break

                        if no_duplicate == True:
                            alldistances.append(nodedistance)
                        else:
                            break

                    if len(alldistances) == size - 1:
                        print(f'Alldistances length = {len(alldistances)} ! voor i: {i}, j: {j}, k: {k}, m: {m}, n: {n}')
                    if  len(alldistances) == size:
                        anchorsfound = True
                        print('Anchors found!')
                        print(node_i)
                        print(node_j)
                        print(node_k)
                        print(node_m)
                        print(node_n)
                        anchors = []
                        anchors.append(node_i)
                        anchors.append(node_j)
                        anchors.append(node_k)
                        anchors.append(node_m)
                        anchors.append(node_n)
                        pickle_out = open(f"Anchors5_s{size}.pickle", "wb")
                        pickle.dump(anchors, pickle_out)
                        pickle_out.close()

                        pickle_out = open(f"Distances_A5_s{size}.pickle", "wb")
                        pickle.dump(alldistances, pickle_out)
                        pickle_out.close()
                    if anchorsfound == True:
                        break
                if anchorsfound == True:
                    break
            if anchorsfound == True:
                break
        if anchorsfound == True:
            break
    if anchorsfound == True:
        break



print('Reached end of script')