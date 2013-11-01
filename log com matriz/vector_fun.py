def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	print(f)
	return(f)

def cria_vector(x, nome, t_abertura):

	#abre arq
	f = abre_arq(nome, t_abertura)
	#x=400, y = 77398

	i = long(0)

	vector = [None]*x
	#construcao do vector, comeca com um nome terremoto+i e o conteudo da linha
	for line in f:
		vector[i] = "terremoto" + str(i), line
		i = i + 1
		if(i == 77398):
			break
	f.close()

	return vector, i


	#k = i % x para fazer grupos