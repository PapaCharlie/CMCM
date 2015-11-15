from wolfram import load_location_dict

class County:
    def __init__(self, county, location, population, neighbors):
        self.county = county
        self.location = location
        self.population = population
        self.neighbors = neighbors

out_of_states = [('OOS1',82),('OOS2',83),('OOS3',84),('OOS4',85),('OOS5',86),('OOS6',87)]

def load_highways():
    with open('../mississippi_county.list','r') as f:
        counties = dict(map(lambda (x,y): (y,x), enumerate(f.readlines())) + out_of_states)
    highways = dict()
    for line in open('../mississippi_graph.csv'):
        line = line.strip().split(',')
        highways[(line[0],line[1])] = int(line[2])
    return highways

if __name__ == '__main__':
    k = load_highways()
    left = set(filter(lambda (x,y): x < y, k))
    right = set(map(lambda (x,y): (y,x), filter(lambda (x,y): x > y, k)))
