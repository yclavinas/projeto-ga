def modificarObservacoes(vetor, s, bins_lat, bins_long, quant_por_grupo):

	import random

	random.seed()

	total_size = bins_long * bins_lat
	N = [0] * s
	modified_vetor = [s*[0] for col in range(total_size)]
	modified_quant_por_grupo = [s*[0] for col in range(total_size)]

	for i in range(s):
		for j in range(total_size):
			r = random.uniform(0,1)
			if (r < 0.005):
				modified_vetor[j][i] = [None]
				modified_quant_por_grupo[j][i] = 0
			else:
				modified_vetor[j][i] = vetor[j]
				modified_quant_por_grupo[j][i] = quant_por_grupo[j]
			N[i] += 1

	return modified_vetor, N, modified_quant_por_grupo