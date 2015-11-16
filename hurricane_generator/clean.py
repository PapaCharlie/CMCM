import pandas as pd
import numpy as np

data = pd.read_csv('hurdat2.csv', dtype = str)
geotags = pd.read_csv('geotags.csv', dtype = str)
num_rows = data.shape[0]

open('hurdat2_cleaned.csv', 'w').close()

row = 0
reading = 1
num_hurricanes = 0

def skip_to_next_hurricane():
	global row
	global reading
	global num_hurricanes
	while row < num_rows and data.ix[row][0][0:2] != 'AL':
		row = row + 1
		reading = reading + 1
	row = row + 1
	num_hurricanes = num_hurricanes + 1

skip_to_next_hurricane()
while row < num_rows:
	if data.ix[row][0][0:2] == 'AL':
		row = row + 1
		num_hurricanes = num_hurricanes + 1
	assert geotags.ix[reading-1][0] == str(row)
	latitude = geotags.ix[reading-1][1]
	longitude = geotags.ix[reading-1][2]
	county = geotags.ix[reading-1][3]
	state = geotags.ix[reading-1][4]
	if state == "Mississippi" and data.ix[row][3].strip() == "HU":
		print data.ix[row][3]
		fileStream = open('hurdat2_cleaned.csv','a')
		fileStream.write(latitude + ",")
		fileStream.write(longitude + ",")
		fileStream.write(county + ",")
		fileStream.write(data.ix[row][6] + ",")
		fileStream.write(str(np.mean(map(float,data.ix[row][8:12]))) + ",")
		fileStream.write(str(np.mean(map(float,data.ix[row][12:16]))) + ",")
		fileStream.write(str(np.mean(map(float,data.ix[row][16:20]))) + "\n")
		fileStream.close()
		skip_to_next_hurricane()
	else:
		row = row + 1
		reading = reading + 1