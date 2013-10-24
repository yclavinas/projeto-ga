from vector_fun import cria_vector

#abertura do arquivo

#chamar funcao para criar matriz a partir do dado lido no arq

vector, i = cria_vector(77398, "jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
	
##########################################

# j-1 e a quant de observacoes de cada grupo
#400(0-399) e a quantidade de grupos

quant_por_grupo = j
total_obs = i

#calculo da prob(abilidade)
prob = (float(quant_por_grupo)/float(total_obs));
print("%.10f" % prob)

