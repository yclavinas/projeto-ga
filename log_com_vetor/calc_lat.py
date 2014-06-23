def calc_lat(nome, t_abertura):
	#abre arq
	f = open(nome, t_abertura)
	#x=400, y = 77398

	menor_lat = str(370)
	maior_lat = str(0.0)

	limit_inf = str(34.8)
	limit_sup = str(57.8)

	for line in f:
	    data = str.split(line)
	    if(data[6] > maior_lat):
	    	if(data[6] >= limit_sup):
		    	maior_lat = data[6]

	f.seek(0,0)

	for line in f:
	    data = str.split(line) 
	    if(data[6] < menor_lat):
	    	if(data[6] >= limit_inf):
		    	menor_lat = data[6]
	  
	f.close()

	return maior_lat, menor_lat
