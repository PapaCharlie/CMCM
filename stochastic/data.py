#!/usr/bin/python

from wolfram import load_location_dict
from numpy import vdot, arccos, degrees, mean
from numpy.linalg import norm

class LonLat:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def away_from_hurricane(self, current_position, hurricane_pos):
        v1 = [current_position.lon - hurricane_pos.lon, current_position.lat - hurricane_pos.lat]
        v2 = [self.lon - current_position.lon, self.lat - current_position.lat]
        return abs(degrees(arccos(vdot(v1,v2)/(norm(v1)*norm(v2))))) < 90

class County:
    def __init__(self, id):
        self.id = id

    def get_neighbors(self):
        return neighbor_map[self.id]

    def viable_neighbors(self, hurricane_loc):
        neighbors = self.get_neighbors()
        return filter(lambda id: locations[id].away_from_hurricane(locations[self.id], hurricane_loc), neighbors)

    def get_county_name(self):
        return filter(lambda k: county_map[k] == self.id, county_map)[0]

    def decrease_pop(self):
        populations[self.id] -= pphpr

    def increase_pop(self):
        populations[self.id] += pphpr

    def escape(self, hurricane_loc, highway_quotas):
        neighbors = self.viable_neighbors(hurricane_loc)
        quotas = map(lambda id: (id, highway_quotas[ordered_tuple(self.id, id)]), neighbors)
        print quotas
        best_route = max(quotas, key = lambda (id, quota): quota)
        if best_route[1] > 0:
            highway_quotas[ordered_tuple(best_route[0], self.id)] -= 1
            self.decrease_pop()
            County(best_route[0]).increase_pop()

county_map = dict()
highways = dict()
locations = dict()
populations = dict()
neighbor_map = dict()

pphpr = 3000 # People per hour per unit of road

def ordered_tuple(k1,k2): return min(k1,k2),max(k1,k2)

def average_huricane_counties(hurricane_counties):
    if type(hurricane_counties[0]) == type(''):
            hurricane_counties = map(lambda s: locations[county_map[s]], hurricane_counties)
    elif type(hurricane_counties[0]) == type(1):
        hurricane_counties = map(lambda id: locations[id], hurricane_counties)
    return LonLat(*map(mean, zip(*map(lambda loc: (loc.lon,loc.lat), hurricane_counties))))

def load_highways():
    global county_map
    global highways
    out_of_states = [('OOS1',82),('OOS2',83),('OOS3',84),('OOS4',85),('OOS5',86),('OOS6',87)]
    with open('../mississippi_county.list') as f:
        county_map = dict(map(lambda (x,y): (y.strip(),x), enumerate(f.readlines())) + out_of_states)
    with open('../mississippi_graph.csv') as graph:
        next(graph)
        for line in graph:
            c1,c2,cap = line.strip().split(',')
            highways[ordered_tuple(county_map[c1], county_map[c2])] = int(cap)

def load_locations():
    global locations
    out_of_states_locations = {'OOS1': (1,1), 'OOS2': (1,1), 'OOS3': (1,1), 'OOS4': (1,1), 'OOS5': (1,1), 'OOS6': (1,1)}
    locs = dict(load_location_dict().items() + out_of_states_locations.items())
    locations = dict(map(lambda c: (county_map[c], LonLat(locs[c][0],-locs[c][1])), locs))

def load_populations():
    global populations
    with open('../mississippi_county_pop.csv') as pops:
        next(pops)
        for line in pops:
            county, pop = line.strip().split(',')
            populations[county_map[county]] = int(pop)

def compute_neighbor_map():
    global neighbor_map
    for id in range(len(locations)):
        keys = map(lambda (x,y): x if x != id else y, filter(lambda (x,y): x == id or y == id, highways))
        # print map(lambda k: (k, highways[(min(id,k), max(id,k))]), keys)
        neighbor_map[id] = map(lambda k: k, keys)

def load_data():
    load_highways()
    load_locations()
    load_populations()
    compute_neighbor_map()

load_data()

if __name__ == '__main__':
    k = County(county_map['Amite'])
    print map(lambda c: County(c).get_county_name(), k.viable_neighbors(locations[county_map['Wilkinson']]))