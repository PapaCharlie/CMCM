import pandas as pd
import numpy as np

data = pd.read_csv('hurdat2_cleaned.csv', dtype=str, header=None)
num_rows = data.shape[0]

open('final.csv', 'w').close()

for row in xrange(num_rows):
	latitude = data.ix[row][0]
	longitude = data.ix[row][1]
	county = data.ix[row][2]
	windspeed = int(data.ix[row][3])
	if windspeed >= 64 and windspeed <= 82:
		category = 1
	elif windspeed >= 83 and windspeed <= 95:
		category = 2
	elif windspeed >= 96 and windspeed <= 112:
		category = 3
	elif windspeed >= 113 and windspeed <= 136:
		category = 4
	else:
		category = 5
	radius = round((0.4718 * windspeed - 7.6557) * 1.852)
	fileStream = open('final.csv','a')
	fileStream.write(latitude + ",")
	fileStream.write(longitude + ",")
	fileStream.write(county + ",")
	fileStream.write(str(windspeed) + ",")
	fileStream.write(str(category) + ",")
	fileStream.write(str(radius) + "\n")
	fileStream.close()