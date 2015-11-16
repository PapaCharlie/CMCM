#!/usr/bin/python

url = "http://api.wolframalpha.com/v2/query?appid=X58777-QPLTKWGKEH&input={county}%20County,%20Mississippi%20(US%20county)"
query = "{county} County, Mississippi  (US county)"

def save_location_dict(d):
    from pickle import dump
    dump(d, open('county_locations.dict', 'wb'))

def load_location_dict():
    from pickle import load
    from os.path import exists
    if exists('county_locations.dict'):
        return load(open('county_locations.dict', 'r'))
    else:
        locations = get_county_locations()
        save_location_dict(locations)
        return locations

def parse_url(google_maps):
    coords = google_maps[google_maps.find("amp;q=")+len("amp;q="):].replace('%20','').replace('%2C',',').replace('N','').replace('W','').replace('S','').replace('E','')
    north, east = map(lambda f:abs(float(f)), coords.split(','))
    return north, -east

def get_county_location(county):
    from urllib2 import urlopen
    page = urlopen(url.format(county = county.replace(' ','%20'))).read()
    u = page.find("http://maps.google.com")
    google_maps = page[u:u + page[u:].find("'")]
    print google_maps
    return parse_url(google_maps)

def read_counties():
    ls = []
    with open('../mississippi_county.list','r') as f:
        for county in f.read().split('\n'):
            ls += [county]
    return ls

def get_county_locations():
    locations = dict()
    for county in read_counties:
        while True:
            try: # lol
                locations[county] = get_county_location(county)
                break
            except:
                pass
    return locations

