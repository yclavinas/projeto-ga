# import sys
import math
from coletar_data import *
from fatorial import *
from log_criacao import *
from calculo_grupos import *
from decimal import *

def log_likelihood(var_coord, num_arquivo):
	
	if (num_arquivo == 2):
		arq_entrada = "testes_7.3.igual.dat"
	else :
		arq_entrada = "jma_cat_2000_2012_Mth2.5_formatted.dat"

	menor_lat, menor_long, bins_lat, bins_long = calc_coordenadas(var_coord, arq_entrada, 'r')

	menor_lat = float(menor_lat)
	menor_long = float(menor_long)
	bins_lat = int(bins_lat)
	bins_long = int(bins_long)

	# print bins_long, bins_lat

	#entra com tamanho do vetor de obs, tamanho do agrupamento e nome do arq e seu mode de abertura
	matriz, expetations, total_obs, quant_por_grupo =coletar_data(arq_entrada, 'r',
	 var_coord, bins_long, bins_lat, menor_lat, menor_long)

	log_likelihood =  [bins_long*[0] for j in range(bins_lat-1)] 
	joint_log_likelihood = long(0)
	descarta_Modelo = False

	for i in range(bins_lat):
		for j in range(bins_long):
			if (quant_por_grupo[i][j] == 0 and expetations[i][j] == 0):
				log_likelihood[i][j] += 1
				log_likelihood[i][j] = log_likelihood[i][j]
			elif (quant_por_grupo[i][j] != 0 and expetations[i][j] == 0):
				log_likelihood[i][j] = Decimal('-Infinity')
				descarta_Modelo = True
			else:
				log_likelihood[i][j] = -expetations[i][j] + (quant_por_grupo[i][j]*math.log10(expetations[i][j])) - (math.log10(fat(quant_por_grupo[i][j])))
			joint_log_likelihood += log_likelihood[i][j]


	#cria um arquivo de log, imprimindo os dados de execucao

	log_criacao(matriz, expetations, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, var_coord)

	return joint_log_likelihood, descarta_Modelo
