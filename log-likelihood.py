#nao tratei lamba = 0, por no momento nao termos o caso -> implementacoes futuras
import sys
import math
from coletar_data import *
from fatorial import *

#77398
#7

tamanho_vetor = int(sys.argv[1])
agrupamento = int(sys.argv[2])

#entra com tamanho do vetor de obs, tamanho do agrupamento e nome do arq e seu mode de abertura
observations, expetations, total_obs, quant_por_grupo =coletar_data(tamanho_vetor, agrupamento,
	"jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')

k = long(0)

#uso log 10 mesmo? estou usando os dados corretos para o calculo?

log_likelihood = [None]*agrupamento


#deve ter um para todos 1o sete e 2o serem do mesmo grupo
#faltou o ultimo passo w! produto dos indv bin likelihood
#falta o joint
for i in range(agrupamento):
	k = i % agrupamento
	log_likelihood[k] = -expetations[k] + (quant_por_grupo[i]*math.log10(expetations[k])) - (math.log10(fat(quant_por_grupo[i])))

print "log_likelihood:"
print(log_likelihood)

joint_log_likelihood = sum(log_likelihood)

print "Joint log_likelihood:"
print(joint_log_likelihood)



#fazer o calculo do bin com long e lat! 0 3 1 2 3 1 2