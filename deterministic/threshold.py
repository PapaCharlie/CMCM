#! /usr/bin/python

import sys
import math
import utils
import pickle as pk
from geopy.distance import vincenty

def threshold(dist, rad, cat):
    if dist/rad > 4:
        return 'Inf'
    th = 0.1 * 2**(dist/rad) / cat
    return str(th)

def dist(p1, p2):
    return vincenty(p1, p2).kilometers

if __name__ == "__main__":
    clat = float(sys.argv[1])
    clong = float(sys.argv[2])
    rad = float(sys.argv[3])
    cat = int(sys.argv[4])

    positions = pk.load(open("county_locations.dict"))
    positions = sorted(positions.items(), key=lambda (k, v) : k)
    positions = map(lambda (k, v) : (v[0], v[1]), positions)
    distances = map(lambda p: dist(p, (clat, clong)), positions)
    thresholds = map(lambda d: threshold(d, rad, cat), distances)
    s = utils.to_matlab(thresholds)
    print s
