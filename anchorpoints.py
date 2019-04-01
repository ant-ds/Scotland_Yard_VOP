#  Script om knopen te zoeken die kunnen dienen als oorsprong
#  in een coordinatensysteem
# 
#  Pseudo om systeem te vinden met N oorsprongen:
#  
#   1. probeer elk paar van N knopen
#   2. bereken voor alle knopen de kortste afstand tot elke oorsprong in het gekozen paar
#   3. kijk of elke coordinaat uniek is


import networkx as nx
import pickle
from game.util import createGraph
import random

debug = 0
size = 199
anchors = 11
gamegraph = createGraph(size)
if nx.is_connected(gamegraph) == False:
    raise "Not connected"

print(f'Searching configuration with {anchors} anchors for size {size}')

anchorsfound = False


for a in range(1, 4000000):
    if a % 2000 == 0:
        print(f'loop {a}')
    
    nodes = random.sample(range(1, size + 1), anchors - 1)
    nodes.append(2)
    alldistances = []
    for l in range(1, size + 1):
        nodedistance = []
        try:
            for anch in range(0, anchors):
                nodedistance.append(nx.shortest_path_length(gamegraph, l, nodes[anch]))

        except:
            print(f'NX: no shortest path for {nodes}')
            continue

        no_duplicate = True
        for distance in alldistances:
            equalamount = 0
            for index in range(0, anchors):
                if nodedistance[index] == distance[index]:
                    equalamount += 1

            if equalamount == anchors:
                no_duplicate = False
                break

        if no_duplicate == True:
            alldistances.append(nodedistance)
        else:
            break

    if len(alldistances) == size:
        anchorsfound = True
        print('Anchors found!')
        print(nodes)
        pickle_out = open(f"Anchors{anchors}_s{size}.pickle", "wb")
        pickle.dump(nodes, pickle_out)
        pickle_out.close()

        pickle_out = open(f"Distances_A{anchors}_s{size}.pickle", "wb")
        pickle.dump(alldistances, pickle_out)
        pickle_out.close()
        
    if anchorsfound == True:
        break


print('Reached end of script')