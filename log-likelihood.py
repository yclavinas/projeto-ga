#nao tratei lamba = 0, por no momento nao termos o caso -> implementacoes futuras
import math
from data_loglike import *

#entra com tamanho do vetor de obs, tamanho do agrupamento e nome do arq e seu mode de abertura
observations, expetations, total_obs, quant_por_grupo =coletar_data(77398, 7,"jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')



k = long(0)

#uso log 10 mesmo? estou usando os dados corretos para o calculo?

log_likelihood = [None]*7

for i in range(7):
	k = i % 7
	log_likelihood[k] = (-expetations[k]) + (quant_por_grupo[i]*math.log10(expetations[k])) - (math.log10(quant_por_grupo[i]))

print(log_likelihood)