import sys
import math
from coletar_data import *
from fatorial import *
from log_criacao import *

#77398
#7
#jma_cat_2000_2012_Mth2.5_formatted
#testes_7.3.igual
#testes_7.diferentes.dat 140, 7

tamanho_vetor = int(sys.argv[1])
agrupamento = int(sys.argv[2])

arq_entrada = "jma_cat_2000_2012_Mth2.5_formatted.dat"


var_coord = float(sys.argv[1])
nome_arquivo = sys.argv[2] #opcoes: 1, 2, 3
tamanho_vetor = int(sys.argv[3]) #limitar o tamanho do vetor por desempenho
# agrupamento = int(sys.argv[2])

if(nome_arquivo == '1'):
	arq_entrada = "jma_cat_2000_2012_Mth2.5_formatted.dat"
elif (nome_arquivo == '2'):
	arq_entrada = "testes_7.3.igual.dat"

#entra com tamanho do vetor de obs, tamanho do agrupamento e nome do arq e seu mode de abertura
observations, expetations, total_obs, quant_por_grupo =coletar_data(tamanho_vetor, agrupamento,
	arq_entrada, 'r')

k = long(0)

#uso log 10 mesmo? estou usando os dados corretos para o calculo?

log_likelihood = [None]*agrupamento


#calcula o log_likelihood
for i in range(agrupamento):
	k = i % agrupamento
	log_likelihood[k] = -expetations[k] + (quant_por_grupo[i]*math.log10(expetations[k])) - (math.log10(fat(quant_por_grupo[i])))

# print "log_likelihood:"
# print(log_likelihood)
# print '\n'

#calcula o joint_log_likelihood
joint_log_likelihood = sum(log_likelihood)

# print "Joint log_likelihood:"
# print(joint_log_likelihood)
# print '\n'

print observations
#cria um arquivo de log, imprimindo os dados de execucao

log_criacao(expetations, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, agrupamento)
