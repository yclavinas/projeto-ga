import random

def modficarObservacoes(matriz, N, s, bins_lat, bins_long, quant_por_grupo):
	modified_matriz = [[[bins_long*[0]] for y in range(bins_lat)] for z in range(s)]
	modified_matriz = modified_matriz * s
	matriz_quantidade = ([bins_long*[0] for y in range(bins_lat)])
	q = 0
	for i in range(s):
		for j in range(bins_long):
			for k in range(bins_lat):
				r = random.uniform(0,1)
				#monte carlo???
				
				if (r < 0.005):
					modified_matriz[j][k] = 0
					#deletar a posicao i,j do vetor
				else:
					#contar a quant depois da mundanca
					modified_matriz[j][k][i] = matriz[j][k]
					#matriz_quantidade[j][k] += quant_por_grupo[j][k]
		print bins_long, bins_lat
		print len(modified_matriz[i]), len(modified_matriz)
		print len(quant_por_grupo[i]), len(quant_por_grupo)
		print len(matriz[i]), len(matriz)
		exit(1)
		print quant_por_grupo
		raw_input()

	return modified_matriz, matriz_quantidade