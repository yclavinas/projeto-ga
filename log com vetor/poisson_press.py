import math

def poisson_press(x,mi):
	if(mi <= 0):
		return
	elif(x >= 0):
		if(x < 1):
			l = math.exp(-mi)
			k = 0
			prob = 1
			while(l < prob):
				k = k + 1
				prob = prob * x
			return (k - 1)
	return 0