import numpy as np
import pandas as pd

import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

from urllib2 import urlopen
import json
import time
def geo_tag(lat, lon, delay=1):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    url += "&key=AIzaSyAe_x2u6tRdLob41KRAvLw6b91MQ3W0NxI"
    try:
        v = urlopen(url).read()
    except Exception as e:
        print e
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

data = pd.read_csv('hurdat2.csv', dtype = str)
num_rows = data.shape[0]

open('geotag_output.csv', 'w').close()

row = 1461
while row < num_rows:
	print "Row: " + str(row)
	if data.ix[row][0][0:2] == 'AL':
		row = row + 1
		pass
	latitude = data.ix[row][4][1:5].strip()
	print latitude
	longitude = "-" + data.ix[row][5][2:6].strip()
	print longitude
	(county,state) = geo_tag(latitude, longitude)
	if county != None:
		print county
	else:
		county= "Unspecified"
		print "Unspecified"
	if state != None:
		print state
	else:
		state = "Ocean"
		print "Ocean"
	print ""
	fileStream = open('geo_tags.csv','a')
	fileStream.write(str(row) + ",")
	fileStream.write(latitude + "," + longitude + ",")
	fileStream.write(county + ",")
	fileStream.write(state + "\r\n")
	fileStream.close()
	row = row + 1