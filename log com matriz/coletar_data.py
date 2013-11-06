from cria_matriz import *

def coletar_data(nome, t_abertura, var_coord, bins_long, bins_lat, menor_lat, menor_long):	

	#chamar funcao para criar o vetor com tamanho max escolhido e a partir do dado lido no arq 
	# ja tem que ter os dados lidos e calcula a quantidade por grupo
	matriz, quant_por_grupo, i = cria_matriz(bins_long, bins_lat, nome, t_abertura, menor_lat, menor_long, var_coord)

	#fazer calculo de total de observacoes
	total_obs = i

	expetations =  [bins_long*[0] for j in range(bins_lat)] 
	for i in range(bins_lat):
		for j in range(bins_long):
			expetations[i][j] = (float(quant_por_grupo[i][j])/float(total_obs));

	return matriz, expetations, total_obs, quant_por_grupo