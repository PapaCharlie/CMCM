#!/usr/bin/python

from sys import argv
from data import County, county_map, average_huricane_counties, highways, populations

highway_quotas = dict()

def flatten(l): return [item for sublist in l for item in sublist]

def main(predictions):
    global highway_quotas
    hurricanes = map(average_huricane_counties, predictions)
    bad_counties = sorted(list(set(flatten(predictions))))
    times = [2*24, 24, 24]

    hours = list()
    for stage in range(3):
        for _ in range(times[stage]):
            highway_quotas = highways.copy()
            second_degree_neighbors = set(flatten(map(lambda id: County(id).get_neighbors(), predictions[stage])))
            second_degree_neighbors = filter(lambda c: not County(c).out_of_state, second_degree_neighbors)
            for neighbor in second_degree_neighbors:
                County(neighbor).escape(hurricanes[stage], highway_quotas)
            pops = map(lambda c: County(c).get_population(), bad_counties)
            hours.append(pops)
            if all(map(lambda p: p == 0, pops)):
                print " ".join(map(lambda c: County(c).get_county_name(), bad_counties))
                return hours

    print " ".join(map(lambda c: County(c).get_county_name(), bad_counties))
    return hours


if __name__ == '__main__':
    if len(argv) >= 2:
        with open(argv[1]) as f:
            args = map(lambda line: map(lambda c: county_map[c], line.strip().split(',')), f.readlines())
    else:
        args = [map(lambda c: county_map[c], ['Hancock','PearlRiver','Harrison','Jackson','Stone','George','Marion','Lamar','Forrest','Perry','Greene']),
                map(lambda c: county_map[c], ['Hancock','PearlRiver','Harrison','Jackson','Stone','George']),
                map(lambda c: county_map[c], ['Hancock','Harrison','Jackson'])]
    hours = main(args)

    s = "m = [" + ";\n".join(map(lambda h: "[" + ",".join(map(str, h)) + "]", hours)) + "];\n"
    open(argv[1] + '.m', 'w').write(s)