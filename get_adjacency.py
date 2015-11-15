#! /usr/bin/python

import csv
import utils

def get_pairs(filename, names):
    with open(filename, 'rb') as csvfile:
        pairs = []
        r = csv.reader(csvfile)
        for row in r:
            a = names[row[0]]
            b = names[row[1]]
            t = (a, b, int(row[2]))
            pairs.append(t)

        return pairs

def get_adjacency(pairs):
    maxtuple = max(pairs, key=maxpair)
    matsize = max(maxtuple) + 1
    mat = [[0 for a in range(matsize)] for a in range(matsize)]
    for p in pairs:
        mat[p[1]][p[0]] = p[2]

    return mat

def maxpair(p):
    return max(p[:2])

if __name__ == "__main__":
    names = utils.get_name_map("mississippi_county.list")
    pairs = get_pairs("mississippi_graph_NS.csv", names)
    mat = get_adjacency(pairs)
    s = utils.to_matlab(mat)
    print s

