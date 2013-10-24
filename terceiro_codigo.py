from vector_fun import cria_vector
from calculo_grupos import calc_grupo

#abertura do arquivo

#chamar funcao para criar o vetor com tamanho max escolhido e a partir do dado lido no arq 
vector, i = cria_vector(77398, "jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
	
#calcula a quantidade de grupo por modulo de um outro numero escolhido
quant_por_grupo = [None]*7
quant_por_grupo = calc_grupo(vector, 7)

total_obs = i

#calculo da prob(abilidade) precisa ser definido
prob = (float(quant_por_grupo)/float(total_obs));
print("%.10f" % prob)

