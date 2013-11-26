import math
from fatorial import fat
from decimal import *
#from log_criacao import log_criacao

def log_likelihood(total_size, quant_por_grupo , expectation, total_obs):

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
			#quant_por_grupo[i] = quant_por_grupo[i]/total_obs
			print quant_por_grupo[i]
			print total_obs
			normalizado =  quant_por_grupo[i]*1000/total_obs
			log_likelihood[i] = -expectation[i] + (normalizado*math.log10(expectation[i])) - (math.log10(fat(normalizado)))

	#calcula o joint_log_likelihood
	joint_log_likelihood = sum(log_likelihood)

	#log_criacao(expectation, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, total_size)

	return joint_log_likelihood, descarta_Modelo