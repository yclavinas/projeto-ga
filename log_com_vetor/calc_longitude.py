def calc_long(nome, t_abertura):
	f = open(nome, t_abertura)
	#x=400, y = 77398

	menor_long = str(370)
	maior_long = str(0.0)

	limit_inf = str(138.8)
	limit_sup = str(161.8)

	for line in f:
	    data = str.split(line)
	    if(data[7] > maior_long):
	    	if(data[7] >= limit_sup):
		    	maior_long = data[7]

	f.seek(0,0)

	for line in f:
	    data = str.split(line) 
	    if(data[7] < menor_long):
	    	if(data[7] >= limit_inf):
		    	menor_long = data[7]
	
	f.close()
	return maior_long, menor_long
