import math
from fatorial import fat
from fatorial import tabela_fatorial
from decimal import *

#from log_criacao import log_criacao

def log_likelihood(total_size, quant_por_grupo, expectation):

	log_likelihood =  [0]*(total_size)
	joint_log_likelihood = long(0)
	descarta_Modelo = False

	for i in range(total_size):
		if (quant_por_grupo[i] == 0 and expectation[i] == 0):
			log_likelihood[i] += 1		
		elif (quant_por_grupo[i] != 0 and expectation[i] == 0):
			log_likelihood[i] = Decimal('-Infinity')
			descarta_Modelo = True
		else:
			log_likelihood[i] = -expectation[i] + (quant_por_grupo[i]*math.log10(expectation[i])) - (math.log10(fat(quant_por_grupo[i])))
			# log_likelihood[i] = -expectation[i] + (quant_por_grupo[i]*math.log10(expectation[i])) - (math.log10(tabela_fatorial(quant_por_grupo[i])))


	#calcula o joint_log_likelihood
	joint_log_likelihood = sum(log_likelihood)

	return log_likelihood, joint_log_likelihood, descarta_Modelo

def dados_observados_R(var_coord, ano_str):

	import random
	from calculo_grupos import calc_coordenadas
	from calcular_expectations import calcular_expectations
	from modificarObservacoes import modificarObservacoes
	from cria_vector import cria_vector
	from cria_random import criar_random

	##inicio coleta e insercao de incertezas
		

	arq_entrada = '../filtro_terremoto_terra.txt'

	#1. Pegar as observacoes e criar o vetor Omega
	#2. Calcular a expectativa das observacoes incertas, vetor de lambdas
	menor_lat, menor_long, bins_lat, bins_long = calc_coordenadas(var_coord, arq_entrada, 'r')

	menor_lat = float(menor_lat)
	menor_long = float(menor_long)
	bins_lat = int(bins_lat)
	bins_long = int(bins_long)
	total_size = 2025

	# print "inicio da criacao do vetor modificado"

	#3.b) sem modificacao
	modified_vetor, quant_por_grupo, N, total_obs, vector_latlong, total_size, N_ano = cria_vector(total_size, arq_entrada, 'r', 
		menor_lat, menor_long, var_coord, ano_str)

	expectations = calcular_expectations(quant_por_grupo, total_size, N)

	joint_log_likelihood, joint_log_likelihood_NaoUso, descarta_Modelo = log_likelihood(total_size, quant_por_grupo, expectations)

	return joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N


