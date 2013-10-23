#abertura do arquivo
f = open("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
print(f)

#criação da matriz que no momento é o grid. Cada ˜bin˜ é uma coluna
matrix = [[0 for x in xrange(100)] for x in xrange(7739)] 

i = 0
j = 0

#construção da matriz, começa com um nome terremoto+i e o conteúdo da linha
for line in f:
	k = i % 100
	matrix[k][j] = "terremoto" + str(i), line
	if k == 99:
		j = j + 1
	i = i + 1
	if i == 9999:
		break
	

