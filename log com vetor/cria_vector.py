def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	print(f)
	return(f)

def cria_vector(tamanho_vetor, nome, t_abertura):

	#abre arq
	f = abre_arq(nome, t_abertura)
	#tamanho_vetor=400, y = 77398

	i = long(0)

	vector = [None]*tamanho_vetor
	#construcao do vector, comeca com um nome terremoto+i e o conteudo da linha
	for line in f:
		vector[i] = "terremoto" + str(i), line
		i += 1
		if(i == tamanho_vetor):
			break
	f.close()
	
	# print vector
	# raw_input("Vetor criado.")
	# print "\n"

	return vector, i


	#k = i % tamanho_vetor para fazer grupos

def cria_vector_desbalanceado(tamanho_vetor, nome, t_abertura):
	#abre arq
	f = abre_arq(nome, t_abertura)
	#tamanho_vetor=400, y = 77398

	i = long(0)
	j = long(1)
	k = long(0)

	vector = [None]*tamanho_vetor
	#construcao do vector, comeca com um nome terremoto+i e o conteudo da linha
	for line in f:
		vector[i] = "terremoto" + str(i), line
		if(j > 20):
			i = i + 1
		elif (j < 20):
			i+=7
		elif (j == 20):
			i = 0
		j+=1
		if(i == tamanho_vetor):
			break
		k += 1
	f.close()
	
	# print vector
	# raw_input("Vetor criado.")
	# print "\n"

	return vector, k



