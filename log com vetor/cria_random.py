import random

def criar_random(total_size, N, multiplicador):
	expectations_simulacao = [None] * (total_size)
	simulacao_quant_por_grupo = [0] * (total_size)


	for l in xrange(total_size):
		expectations_simulacao[l] = random.random()
		simulacao_quant_por_grupo[l] = int((random.random()*multiplicador))
	return expectations_simulacao, simulacao_quant_por_grupo