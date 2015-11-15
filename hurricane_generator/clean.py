import pandas as pd
import numpy as np

import time

from geography import get_state

data = pd.read_csv('hurdat2.csv', dtype = str)
num_rows = data.shape[0]

open('hurdat2_cleaned.csv', 'w').close()

row = 0
num_hurricanes = 0

def skip_to_next_hurricane():
	global row
	global num_hurricanes
	while row < num_rows and data.ix[row][0][0:2] != 'AL':
		row = row + 1
	row = row + 1
	num_hurricanes = num_hurricanes + 1
	if row < num_rows:
		print "\r\nHurricane " + str(num_hurricanes) + "/1793"

skip_to_next_hurricane()
while row < num_rows:
	if data.ix[row][0][0:2] == 'AL':
		row = row + 1
		num_hurricanes = num_hurricanes + 1
		if row < num_rows:
			print "\r\nHurricane " + str(num_hurricanes) + "/1793"
		pass
	latitude = data.ix[row][4][1:5]
	longitude = "-" + data.ix[row][5][2:6]
	state = get_state(latitude, longitude)
	if state != None:
		print state
	else:
		print "Ocean"
	if state == "Mississippi" and data.ix[row][3] == "HU":
		fileStream = open('hurdat2_cleaned.csv','a')
		fileStream.write(latitude + "," + longitude + ",")
		fileStream.write(get_county(latitude, longitude) + ",")
		fileStream.write(data.ix[row][6] + ",")
		fileStream.write(str(mean(int(data.ix[row][8:12]))) + ",")
		fileStream.write(str(mean(int(data.ix[row][12:16]))) + ",")
		fileStream.write(str(mean(int(data.ix[row][16:20]))) + "\n")
		fileStream.close()
		skip_to_next_hurricane()
	else:
		row = row + 1