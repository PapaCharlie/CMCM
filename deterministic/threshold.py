#! /usr/bin/python

import sys
import math
import utils
import pickle as pk
from geopy.distance import vincenty

def threshold(dist, rad, cat):
    if dist/rad > 3:
        return 1000000
    if cat == 1:
        return 0.5
    th = 0.1 * 2**(dist/rad) / cat
    return th

def dist(p1, p2):
    return vincenty(p1, p2).kilometers

def compute_thresholds(clat, clong, rad, cat):
    positions = pk.load(open("county_locations.dict"))
    positions = sorted(positions.items(), key=lambda (k, v) : k)
    positions = map(lambda (k, v) : (v[0], v[1]), positions)
    distances = map(lambda p: dist(p, (clat, clong)), positions)
    thresholds = map(lambda d: threshold(d, rad, cat), distances)
    return thresholds

if __name__ == "__main__":
    clat = float(sys.argv[1])
    clong = float(sys.argv[2])
    rad = float(sys.argv[3])
    cat = int(sys.argv[4])

    thresholds = compute_thresholds(clat, clong, rad, cat)
    s = utils.to_matlab(thresholds, '')
    s = s.replace('\n', '')
    s = s[:-1]
    print s

