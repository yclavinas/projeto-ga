f = open("1.dat", 'r')
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
	matrix[k][j] = "terremoto" + str(i)
	#print(matrix[k][j])
	if k == 99:
		j = j + 1
	i = i + 1
	if i == 9999:
		break
	
	

for ncols in xrange(i):
	for nrows in xrange(j):
		#print matrix[99][nrows]
		a = 0
		#raw_input('press enter!')
		
print("ncols = ",ncols)
print("i = ",i)

print("nrows = ",nrows)
print("j = ",j)
