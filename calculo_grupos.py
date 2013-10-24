def calc_grupo(vector, modulador):
	i = long(0)
	aux = [0]*7
	final = len(vector)
	for i in xrange(final):
		k = i % modulador
		if (vector[i] != None):
			aux[k] = aux[k] + 1
	return aux