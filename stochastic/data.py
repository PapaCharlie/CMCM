#!/usr/bin/python

from wolfram import load_location_dict

county_map = dict()
highways = dict()
locations = dict()
populations = dict()

pphpr = 3000 # People per hour per unit of road

def load_highways():
    global county_map
    global highways
    out_of_states = [('OOS1',82),('OOS2',83),('OOS3',84),('OOS4',85),('OOS5',86),('OOS6',87)]
    with open('../mississippi_county.list') as f:
        county_map = dict(map(lambda (x,y): (y.strip(),x), enumerate(f.readlines())) + out_of_states)
    for line in open('../mississippi_graph.csv'):
        c1,c2,cap = line.strip().split(',')
        highways[(county_map[c1], county_map[c2])] = int(cap)

def load_locations():
    global locations
    out_of_states_locations = {'OOS1': (1,1), 'OOS2': (1,1), 'OOS3': (1,1), 'OOS4': (1,1), 'OOS5': (1,1), 'OOS6': (1,1)}
    locs = dict(load_location_dict().items() + out_of_states_locations.items())
    locations = dict(map(lambda c: (county_map[c], locs[c]), locs))

def load_populations():
    global populations
    for line in open('../mississippi_county_pop.csv'):
        county, pop = line.strip().split(',')
        populations[county_map[county]] = pop

load_highways()
load_locations()
load_populations()
