#! /usr/bin/python

import csv

def get_name_map(filename):
    with open(filename, 'rb') as fh:
        h = {}
        counter = 0
        for line in fh:
            h[line.strip()] = counter
            counter += 1

        return h

def get_pairs(filename, names):
    with open(filename, 'rb') as csvfile:
        pairs = []
        r = csv.reader(csvfile)
        for row in r:
            a = names[row[0]]
            b = names[row[1]]
            t = (a, b, row[2])
            pairs.append(t)

        return pairs

def get_adjacency(pairs):
    matsize = max(pairs, key=maxpair)
    mat = [[0 for a in range(matsize)] for a in range(matsize)]
    for p in pairs:
        mat[p[1]][p[0]] = p[2]

    return mat

def maxpair(p):
    return max(p[:2])

def to_matlab(mat):
    s = '['
    for row in mat:
        s += str(row) + ';'

    return s + ']'

if __name__ == "__main__":
    names = get_name_map("mississippi_county.list")
    pairs = get_pairs("graph.csv", names)
    mat = get_adjacency(pairs)
    s = to_matlab(mat)
    print s

