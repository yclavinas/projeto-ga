def cria_vector(total_size, nome, t_abertura, menor_lat, menor_long, var_coord):

	from calculo_grupos import calc_grupo_coord
	import random

	# random.seed()

	#abre arq
	f = open(nome, t_abertura)
	#tamanho_vetor=400, y = 77398

	N = long(0)
	total_obs = long(0)

	vector = [None]*(total_size)
	vector_quantidade = [0]*(total_size)
	vector_latlong = [None]*(total_size)

	for line in f:
		# r = random.uniform(0,1)
		# if (r > 0.01):

		aux2 = str.split(str(line))
		obs_menor_long = float(aux2[7])
		obs_menor_lat = float(aux2[6])

		x_long, y_lat = calc_grupo_coord(obs_menor_long, obs_menor_lat, menor_lat, menor_long, var_coord)
				
		vector_latlong[int(x_long*y_lat)] = aux2[6]+", "+aux2[7]

		vector[int(x_long*y_lat)] = line
		vector_quantidade[int(x_long*y_lat)] += 1
		N += 1
		total_obs += 1
	f.close()

	return vector, vector_quantidade, N, total_obs, vector_latlong
