def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	print(f)
	return(f)

def cria_matriz(x, y, nome, t_abertura):

	#abre arq
	f = abre_arq(nome, t_abertura)
	#x=400, y = 77398
	x1 = x
	matrix = [[0 for x in xrange(x1)] for y in xrange(y)] 

	i = long(0)
	j = long(0)

	#construcao da matriz, comeca com um nome terremoto+i e o conteudo da linha
	for line in f:
		k = i % x
		matrix[k][j] = "terremoto" + str(i), line
		if k == x-1:
			j = j + 1
		i = i + 1
		if i == 100000:
			break
	f.close()

	
	return matrix, i, j