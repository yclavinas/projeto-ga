import random

def criar_random(bins_lat, bins_long):
	expetations =  [bins_long*[0] for j in range(bins_lat)] 
	for i in range(bins_lat):
		for j in range(bins_long):
			expetations[i][j] = random.uniform(0,1)
	return expetations

