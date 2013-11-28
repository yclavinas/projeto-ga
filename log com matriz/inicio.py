import random
from calculo_grupos import calc_coordenadas
from coletar_data import coletar_data
from log_likelihood import log_likelihood
from modficarObservacoes import modficarObservacoes


var_coord = 0.5
arq_entrada = 'jma_cat_2000_2012_Mth2.5_formatted.dat'

#1. Pegar as observacoes e criar o vetor Omega
#2. Calcular a expectativa das observacoes incertas, vetor de lambdas
menor_lat, menor_long, bins_lat, bins_long = calc_coordenadas(var_coord, arq_entrada, 'r')

menor_lat = float(menor_lat)
menor_long = float(menor_long)
bins_lat = int(bins_lat)
bins_long = int(bins_long)

#entra com tamanho do vetor de obs, tamanho do agrupamento e nome do arq e seu mode de abertura
matriz, expetations, total_obs, quant_por_grupo =coletar_data(arq_entrada, 'r',
 var_coord, bins_long, bins_lat, menor_lat, menor_long)

#3. Modifica-lo para introduzir incertezas S vezes, gerando um vetor de tamanho S de omega~(modificado). 
random.seed(123)
s = random.randint(0, 100)
N = [0]* s
modified_matriz, total_obs = modficarObservacoes(matriz, N, s, bins_lat, bins_long, quant_por_grupo)

#4. Calcular o log-likelihood do Modelo (1)