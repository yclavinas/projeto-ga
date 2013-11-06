def abre_arq(nome, t_abertura):
	f = open(nome, t_abertura)
	return(f)

def cria_matriz(bins_long, bins_lat, nome, t_abertura, menor_lat, menor_long, var_coord):
	from calculo_grupos import calc_grupo_coord
	#abre arq
	f = abre_arq(nome, t_abertura)
	
	matriz_dados = [bins_long*[0] for y in range(bins_lat)]
	matriz_quantidade = [bins_long*[0] for x in range(bins_lat)] 

	i = long(0)

	#construcao da matriz, comeca com um nome terremoto+i e o conteudo da linha
	for line in f:
		x_long, y_lat = calc_grupo_coord(line, menor_lat, menor_long, var_coord)

		x_long = int(x_long)
		y_lat = int(y_lat)

		matriz_dados[x_long][y_lat] = line
		matriz_quantidade[x_long][y_lat] += 1 

		i += 1
		if(i % 100000 == 0):
			print i
	
	f.close()
	
	return matriz_dados, matriz_quantidade, i