#abertura do arquivo
f = open("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
print(f)

#criacao da matriz que no momento e o grid. Cada bin e uma coluna

matrix = [[0 for x in xrange(1000)] for y in xrange(77398)] 

i = 0
j = 0
i = long(i)
j = long(j)
#construcao da matriz, comeca com um nome terremoto+i e o conteudo da linha
for line in f:
	k = i % 1000
	matrix[k][j] = "terremoto" + str(i), line
	if k == 99:
		j = j + 1
	i = i + 1
	if i == 77398:
		break
	
print(i)
print(j)