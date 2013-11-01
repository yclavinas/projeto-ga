#para ficar mais facil, colocar as funcoes definir o obj com o nome da funcao
def coletar_data(tamanho_vetor, agrupamento, nome, t_abertura):

	from cria_vector import *
	from calculo_grupos import calc_grupo

	#abertura do arquivo

	#chamar funcao para criar o vetor com tamanho max escolhido e a partir do dado lido no arq 
	if (nome == 'testes_7.diferentes.dat'):
		vector, i = cria_vector_desbalanceado(tamanho_vetor, nome, t_abertura)
	else:
		vector, i = cria_vector(tamanho_vetor, nome, t_abertura)
		
	#calcula a quantidade de grupo por modulo de um outro numero escolhido
	quant_por_grupo = [None]*agrupamento
	quant_por_grupo = calc_grupo(vector, agrupamento)

	# print quant_por_grupo
	# raw_input("Quantidade por grupo.")
	# print '\n'

	#fazer calculo de total de observacoes
	total_obs = i
	
	# print total_obs
	# raw_input("Total de observacoes.")
	# print '\n'

	#calculo da prob(abilidade) precisa ser definido

	prob = [None]*agrupamento
	for l in xrange(agrupamento):
		print "quant_por_grupo, total_obs"
		print quant_por_grupo[l], total_obs
		prob[l] = (float(quant_por_grupo[l])/float(total_obs));
		
	# 	print("%.10f" % prob[l])
	# 	raw_input("Probabilidade."+str(l))
	# print '\n'

	return vector, prob, total_obs, quant_por_grupo