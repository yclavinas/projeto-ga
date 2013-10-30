#para ficar mais facil, colocar as funcoes definir o obj com o nome da funcao
def coletar_data(vector_size, vector_group, nome, t_abertura):

	from cria_vector import cria_vector
	from calculo_grupos import calc_grupo

	#abertura do arquivo

	#chamar funcao para criar o vetor com tamanho max escolhido e a partir do dado lido no arq 
	vector, i = cria_vector(vector_size, nome, t_abertura)
		
	#calcula a quantidade de grupo por modulo de um outro numero escolhido
	quant_por_grupo = [None]*vector_group
	quant_por_grupo = calc_grupo(vector, vector_group)

	total_obs = i

	#calculo da prob(abilidade) precisa ser definido

	prob = [None]*vector_group
	for l in xrange(vector_group):
		prob[l] = (float(quant_por_grupo[l])/float(total_obs));
		#print("%.10f" % prob[l])

	return vector, prob, total_obs, quant_por_grupo