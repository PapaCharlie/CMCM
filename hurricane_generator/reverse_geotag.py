import numpy as np
import pandas as pd

import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')


from geography import geo_tag

data = pd.read_csv('hurdat2.csv', dtype = str)
num_rows = data.shape[0]

open('geo_tags.csv', 'w').close()

row = 1450
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