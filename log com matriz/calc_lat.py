def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	#print(f)
	return(f)

def calc_lat(nome, t_abertura):
	#abre arq
	f = abre_arq("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
	#x=400, y = 77398

	menor_lat = str(60.3052)
	maior_lat = 0.0

	for line in f:
	    data = str.split(line)
	    if(data[1] > maior_lat):
	    	maior_lat = data[1]

	f.seek(0,0)

	for line in f:
	    data = str.split(line) 
	    if(data[1] < menor_lat):
	    	menor_lat = data[1]

	f.close()
	return maior_lat, menor_lat
