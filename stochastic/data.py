#!/usr/bin/python

from wolfram import load_location_dict
from numpy import vdot, arccos, degrees, mean
from numpy.linalg import norm

class LonLat:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def __str__(self):
        return "(%0.5F,%0.5F)"%(self.lon,self.lat)

    def __repr__(self):
        return "LonLat(%0.5F,%0.5F)"%(self.lon,self.lat)

    def away_from_hurricane(self, current_position, hurricane_pos):
        v1 = [current_position.lon - hurricane_pos.lon, current_position.lat - hurricane_pos.lat]
        v2 = [self.lon - current_position.lon, self.lat - current_position.lat]
        return (abs(degrees(arccos(vdot(v1,v2)/(norm(v1)*norm(v2))))) < 90) #and (self.lat >= current_position.lat or self.lon >= current_position.lon)

class County:
    def __init__(self, id):
        self.id = id
        self.out_of_state = id > 82

    def __str__(self): return "County(%s|%d|%d)"%(self.get_county_name(),self.id, self.get_population())

    def __repr__(self): return "County(%s|%d|%d)"%(self.get_county_name(),self.id, self.get_population())

    def get_location(self): return locations[self.id]

    def get_county_name(self): return filter(lambda k: county_map[k] == self.id, county_map)[0]

    def get_neighbors(self): return neighbor_map[self.id]

    def get_population(self): return populations[self.id]

    def viable_neighbors(self, hurricane_loc):
        neighbors = self.get_neighbors()
        return filter(lambda id: locations[id].away_from_hurricane(locations[self.id], hurricane_loc) or locations[id].lat > self.get_location().lat, neighbors)

    def move_pop(self, neighbor):
        diff = min(pphpr, populations[self.id])
        populations[self.id] -= diff
        populations[neighbor] += diff

    def escape(self, hurricane_loc, highway_quotas):
        if self.get_population() > 0:
            neighbors = self.viable_neighbors(hurricane_loc)
            if len(neighbors) > 0:
                quotas = map(lambda id: (id, highway_quotas[ordered_tuple(self.id, id)]), neighbors)
                # best_route = max(quotas, key = lambda (id, quota): County(id).get_location().lat)
                best_route = max(quotas, key = lambda (id, quota): quota)
                while highway_quotas[ordered_tuple(best_route[0], self.id)] > 0:
                    highway_quotas[ordered_tuple(best_route[0], self.id)] -= 1
                    self.move_pop(best_route[0])
            else:
                northmost = max(self.get_neighbors(), key = lambda c: County(c).get_location().lat)
                while highway_quotas[ordered_tuple(northmost, self.id)] > 0:
                    highway_quotas[ordered_tuple(northmost, self.id)] -= 1
                    self.move_pop(northmost)


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
    out_of_state = [('OOS1',82),('OOS2',83),('OOS3',84),('OOS4',85),('OOS5',86),('OOS6',87)]
    with open('../mississippi_county.list') as f:
        county_map = dict(map(lambda (x,y): (y.strip(),x), enumerate(f.readlines())) + out_of_state)
    for line in open('../mississippi_graph_NS.csv'):
        c1,c2,cap = line.strip().split(',')
        highways[ordered_tuple(county_map[c1], county_map[c2])] = int(cap)
    for line in open('../mississippi_graph_EW.csv'):
        c1,c2,cap = line.strip().split(',')
        highways[ordered_tuple(county_map[c1], county_map[c2])] = int(cap)

def load_locations():
    global locations
    out_of_state_locations = {
        'OOS1': (35.362031, -89.121045),
        'OOS2': (34.433951, -180),
        'OOS3': (32.240532, -180),
        'OOS4': (30.703905, -90.626172),
        'OOS5': (31.886736, 0),
        'OOS6': (33.769867, 0)
    }
    locs = dict(load_location_dict().items() + out_of_state_locations.items())
    locations = dict(map(lambda c: (county_map[c], LonLat(locs[c][0],locs[c][1])), locs))

def load_populations():
    global populations
    out_of_state_populations = {'OOS1': 0,'OOS2': 0,'OOS3': 0,'OOS4': 0,'OOS5': 0,'OOS6': 0}
    populations = dict(map(lambda c: (county_map[c], out_of_state_populations[c]), out_of_state_populations))
    for line in open('../mississippi_county_pop.csv'):
        county, pop = line.strip().split(',')
        populations[county_map[county]] = int(pop)

def compute_neighbor_map():
    global neighbor_map
    for id in range(len(locations)):
        keys = map(lambda (x,y): x if x != id else y, filter(lambda (x,y): x == id or y == id, highways))
        neighbor_map[id] = map(lambda k: k, keys)

def load_data():
    load_highways()
    load_locations()
    load_populations()
    compute_neighbor_map()

load_data()

if __name__ == '__main__':
    from sys import argv
    if len(argv) >= 2:
        c = eval(argv[1])
        print County(c)
        print County(c).get_population()