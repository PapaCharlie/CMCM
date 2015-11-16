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

def get_edges(filename, names):
    with open(filename, 'rb') as csvfile:
        pairs = []
        r = csv.reader(csvfile)
        for row in r:
            a = names[row[0]]
            b = names[row[1]]
            t = (a, b, int(row[2]))
            pairs.append(t)

        return pairs

def to_matlab(mat, mname = 'm'):
    s = mname + ' = ['
    for row in mat:
        s += str(row) + ';\n'

    return s + '];'

