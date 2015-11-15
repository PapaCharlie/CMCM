#! /usr/bin/python

import csv

def get_population(filename):
    with open(filename, 'rb') as fh:
        r = csv.DictReader(fh)
        pairs = []
        for row in r:
            t = (row['NAME'], int(row['POPULATION']))
            pairs.append(t)

        return pairs

def get_name_map(filename):
    with open(filename, 'rb') as fh:
        h = {}
        counter = 0
        for line in fh:
            h[line.strip()] = counter
            counter += 1

        return h

def to_matlab(mat, mname = 'm'):
    s = mname + ' = ['
    for row in mat:
        s += str(row) + ';\n'

    return s + '];'

