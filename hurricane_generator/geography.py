from urllib2 import urlopen
import json
import time
def geo_tag(lat, lon, delay=1):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    url += "&key=AIzaSyAe_x2u6tRdLob41KRAvLw6b91MQ3W0NxI"
    try:
        v = urlopen(url).read()
    except:
        print "RECONNECT"
        time.sleep(delay)
        return geo_tag(lat, lon, delay + 1)
    j = json.loads(v)
    state = county = None
    if len(j['results']) > 0:
        components = j['results'][0]['address_components']
        for c in components:
            if "administrative_area_level_1" in c['types']:
                state = c['long_name']
            if "administrative_area_level_2" in c['types']:
                county = c['long_name']
    return (county,state)

# print geo_tag(40.1308,-75.5192)