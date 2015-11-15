#! /usr/bin/python

import utils

def get_mat(names, population):
    mat = []
    for t in population:
        mat.append(t[1])
    return mat

if __name__ == "__main__":
    populations = utils.get_population("mississippi_county_pop.csv")
    names = utils.get_name_map("mississippi_county.list")
    mat = get_mat(names, populations)
    s = utils.to_matlab(mat, 'pops')
    print s
