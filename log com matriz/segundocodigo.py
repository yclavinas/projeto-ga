#abertura do arquivo
f = open("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
print(f)

#criacao da matriz que no momento e o grid. Cada bin e uma coluna
#77398
matrix = [[0 for x in xrange(400)] for y in xrange(77398)] 

i = long(0)
j = long(0)
#i = long(i)
#j = long(j)
#construcao da matriz, comeca com um nome terremoto+i e o conteudo da linha
for line in f:
	k = i % 400
	matrix[k][j] = "terremoto" + str(i), line
	if k == 399:
		j = j + 1
	i = i + 1
	if i == 100000:
		break
	
##########################################

# j-1 e a quant de observacoes de cada grupo
#400(0-399) e a quantidade de grupos

quant_por_grupo = j
total_obs = i

#calculo da prob(abilidade)
prob = (float(quant_por_grupo)/float(total_obs));
print("%.10f" % prob)

f.close()