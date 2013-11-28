def calc_lat(nome, t_abertura):
	#abre arq
	f = open(nome, t_abertura)
	#x=400, y = 77398

	menor_lat = str(60.3052)
	maior_lat = 0.0

	for line in f:
	    data = str.split(line)
	    if(data[6] > maior_lat):
	    	maior_lat = data[6]

	f.seek(0,0)

	for line in f:
	    data = str.split(line) 
	    if(data[6] < menor_lat):
	    	menor_lat = data[6]
	  
	f.close()

	return maior_lat, menor_lat
