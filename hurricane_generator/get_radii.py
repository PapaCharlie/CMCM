import pandas as pd
import numpy as np

data = pd.read_csv('hurdat2.csv', dtype = str)
num_rows = data.shape[0]

open('wind_radii.csv', 'w').close()

row = 44300
while row < num_rows:
	if data.ix[row][0][0:4] == '2004':
		wind_speed = data.ix[row][6]
		wind_radius = np.mean(map(float,data.ix[row][16:20]))
		if not wind_radius > 0:
			wind_radius = np.mean(map(float,data.ix[row][12:16])) 
		if not wind_radius > 0:
			wind_radius = np.mean(map(float,data.ix[row][8:12]))
		if wind_radius > 0:
			fileStream = open('wind_radii.csv','a')
			fileStream.write(wind_speed + ",")
			fileStream.write(str(wind_radius) + "\n")
			fileStream.close()
	row = row + 1