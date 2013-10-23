f = open("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
print(f)

matrix = [[0 for x in xrange(100)] for x in xrange(7739)] 
i = 0
j = 0
for line in f:
	data = str.split(line)
	#print (data[0])
	#print (data[1])
	
	k = i % 100

	#raw_input('press enter!')
	matrix[k][j] = "terremoto" + str(i), line
	#print(matrix[k][j])
	if k == 99:
		j = j + 1
	i = i + 1
	if i == 9999:
		break
	
	

for ncols in xrange(i):
	for nrows in xrange(j):
		print matrix[0][nrows]
		raw_input('press enter!')
		
print("i = ",i)
print("j = ",j)
