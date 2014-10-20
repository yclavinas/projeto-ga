# import sys
import math

from fatorial import *
from log_criacao import *

from decimal import *

def log_likelihood(bins_long, bins_lat, quant_por_grupo , expetations):

	log_likelihood =  [bins_long*[0] for j in range(bins_lat)] 
	joint_log_likelihood = long(0)
	descarta_Modelo = False

	for i in range(bins_long):
		for j in range(bins_lat):
			if (quant_por_grupo[i][j] == 0 and expetations[i][j] == 0):
				log_likelihood[i][j] += 1
			elif (quant_por_grupo[i][j] != 0 and expetations[i][j] == 0):
				log_likelihood[i][j] = Decimal('-Infinity')
				descarta_Modelo = True
			else:
				log_likelihood[i][j] = -expetations[i][j] + (quant_por_grupo[i][j]*math.log10(expetations[i][j])) - (math.log10(fat(quant_por_grupo[i][j])))
			joint_log_likelihood += log_likelihood[i][j]

	#cria um arquivo de log, imprimindo os dados de execucao

	#log_criacao(matriz, expetations, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, var_coord)

	return joint_log_likelihood, descarta_Modelo
