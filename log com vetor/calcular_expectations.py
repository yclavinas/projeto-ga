#para ficar mais facil, colocar as funcoes definir o obj com o nome da funcao
def calcular_expectations(modified_quant_por_grupo, total_size, menor_lat, menor_long, N):

	expectations = [None] * (total_size)

	for l in xrange(total_size):
		# expetations[l] = (float(modified_quant_por_grupo[l])/float(N[l]))
		expectations[l] = (float(modified_quant_por_grupo[l])/float(N))
	
	return expectations