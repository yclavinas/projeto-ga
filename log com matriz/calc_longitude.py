
def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	#print(f)
	return(f)

def calc_long(nome, t_abertura):
	#abre arq
	f = abre_arq("jma_cat_2000_2012_Mth2.5_formatted.dat", 'r')
	#x=400, y = 77398

	menor_long = str(60.3052)
	maior_long = 0.0

	for line in f:
	    data = str.split(line)
	    if(data[0] > maior_long):
	    	maior_long = data[0]

	f.seek(0,0)

	for line in f:
	    data = str.split(line) 
	    if(data[0] < menor_long):
	    	menor_long = data[0]
	
	f.close()
	return maior_long, menor_long
