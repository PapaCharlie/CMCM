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

def to_matlab(mat):
    s = 'm = ['
    for row in mat:
        s += str(row) + ';'

    return s + ']'

if __name__ == "__main__":
    names = get_name_map("mississippi_county.list")
    pairs = get_pairs("mississippi_graph_NS.csv", names)
    mat = get_adjacency(pairs)
    s = to_matlab(mat)
    print s

