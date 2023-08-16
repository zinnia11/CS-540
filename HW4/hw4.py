import numpy as np
import csv
import math
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

# six dimensional feature vector: HP, Attack, Defense, Sp. Atk, Sp.Def, Speed
# cluster the Pokemon represented by the vector 

def load_data(filepath):
    # read file into a list of dictionaries (like hashtables of key value pairs)
    with open(filepath, newline='') as file :
        d = csv.DictReader(file)
        return list(d)
    pass

def calc_features(row):
    # parse one given dict into a six featured array in a particular order
    atk = int(row['Attack'])
    sp_atk = int(row['Sp. Atk'])
    spd = int(row['Speed'])
    defs = int(row['Defense'])
    sp_defs = int(row['Sp. Def'])
    hp = int(row['HP'])
    return np.array([atk, sp_atk, spd, defs, sp_defs, hp])
    pass

# input: list of feature array as given above
# output: array of size (n-1)x4 where n is size of input list
    # 0, 1 -> indices of merged clusters on iteration i
    # 2 -> linkage distance between the two clusters
    # 3 -> size of new cluster (num of Pokemon)
def hac(features):
    l = len(features)
    result = np.zeros((l-1, 4))
    distances = np.zeros((l, l))
    visited = [] # array to keep track of visited nodes
    merged = []
    
    # calculate distances in a matrix
    for i in range(0, l):
        for j in range(0, l):
            if (i != j):
                distances[i,j] = math.sqrt(sum(np.square(features[i] - features[j])))
    # continue to expand matrix with the clusters and distances. 

    # copy to change to find correct merges
    distances_calc = distances.copy()
    # begin merging and calculations
    for n in range(0, l-1):
        # mask out all zeros, and identify the index of lowest value
        mask = np.ma.masked_array(distances_calc, mask=distances_calc==0)
        # the following line references: 
        # https://stackoverflow.com/questions/30180241/numpy-get-the-column-and-row-index-of-the-minimum-value-of-a-2d-array
        c1, c2 = divmod(mask.argmin(), mask.shape[1]) 

        # the first three values in the result
        result[n][0] = c1
        result[n][1] = c2
        result[n][2] = distances[c1][c2]
        # add together the cluster sizes
        # while gathering points that are in the cluster
        hold = []
        if (c1 < l and c2 < l):
            result[n][3] = 2
            hold = hold + [c1,c2]
        else:
            if (c1 > l-1):
                result[n][3] = result[n][3]+result[c1-l][3]
                if (isinstance(hold, np.ndarray)):
                    hold = hold.tolist()
                hold = hold + visited[c1-l]
            else:
                result[n][3] = result[n][3]+1
                hold.append(c1)
            if (c2 > l-1):
                result[n][3] = result[n][3]+result[c2-l][3]
                if (isinstance(hold, np.ndarray)):
                    hold = hold.tolist()
                hold = hold + visited[c2-l]
            else:
                result[n][3] = result[n][3]+1
                hold.append(c2)

        # merged clusters
        merged.append([c1,c2])
        # all of the points in the new cluster
        visited.append(hold)
        # calculate distances to the new cluster
        new = np.zeros(n+l)
        for x in range(0, len(distances)):
            allpd = []
            # using gathered points, calculate distance between
            for v in hold:
                if (x != c1 and x != c2):
                    allpd.append(distances[v][x])
                    new[x] = max(allpd)

        # add a row and column for the new cluster
        distances = np.vstack((distances, new))
        distances = np.hstack((distances, np.reshape(np.append(new, 0), (-1, 1))))
        distances_calc = np.vstack((distances_calc, new))
        distances_calc = np.hstack((distances_calc, np.reshape(np.append(new, 0), (-1, 1))))
        # clear the calc matric rows to 0
        for c in merged:
            distances_calc[:,c] = 0
            distances_calc[c] = 0
        
    #result = sch.linkage(features, method='complete', metric="euclidean")
    return result
    pass

def imshow_hac(Z):
    graph = sch.dendrogram(Z)
    plt.show()
    pass

