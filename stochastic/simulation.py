#!/usr/bin/python

from sys import argv
from data import County, county_map, average_huricane_counties, highways

hours = -4*24

highway_quotas = dict()

def flatten(l): return [item for sublist in l for item in sublist]

def main(predictions):
    global highway_quotas
    hurricanes = map(average_huricane_counties, predictions)
    print hurricanes
    times = [2*24, 24, 24]

    for stage in range(0,3):
        for _ in range(times[stage]):
            highway_quotas = highways.copy()
            second_degree_neighbors = set(flatten(map(lambda id: County(id).get_neighbors(), predictions[stage])))
            second_degree_neighbors = filter(lambda c: not County(c).out_of_state, second_degree_neighbors)
            for neighbor in second_degree_neighbors:
                print neighbor
                County(neighbor).escape(hurricanes[stage], highway_quotas)

if __name__ == '__main__':
    global args
    if len(argv) > 2:
        with open(argv[1]) as f:
            args = map(lambda line: map(lambda c: county_map[c], line.strip().split(',')), f.readlines())
    else:
        args = [map(lambda c: county_map[c], ['Hancock','PearlRiver','Harrison','Jackson','Stone','George','Marion','Lamar','Forrest','Perry','Greene']),
                map(lambda c: county_map[c], ['Hancock','PearlRiver','Harrison','Jackson','Stone','George']),
                map(lambda c: county_map[c], ['Hancock','Harrison','Jackson'])]
    main(args)

