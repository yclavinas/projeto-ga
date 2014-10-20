def calculo_totalObservacoes(vector, agrupamento,tamanho_vetor):
	j = 0
	k = 0
	totalObservacoes = [0] * agrupamento	
	for i in vector:
		while (vector[j] != None):
			totalObservacoes[k] += 1
			j += agrupamento
			if (j >= tamanho_vetor):
				break
		k += 1
		j = k
		if (k >= agrupamento):
			break

	return totalObservacoes
