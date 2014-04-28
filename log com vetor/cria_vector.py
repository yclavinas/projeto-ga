def cria_vector(total_size, nome, t_abertura, menor_lat, menor_long, var_coord):

	from calculo_grupos import calc_grupo_coord
	import random

	f = open(nome, t_abertura)

	N = 0
	total_obs = long(0)

	vector = [None]*(total_size)
	vector_quantidade = [0]*(total_size)
	vector_latlong = [None]*(total_size)

	for line in f:
		aux2 = str.split(str(line))
		obs_menor_long = float(aux2[7])
		obs_menor_lat = float(aux2[6])

		x_long, y_lat, index = calc_grupo_coord(obs_menor_long, obs_menor_lat, menor_lat, menor_long, var_coord)
				
		vector[index] = line
		vector_quantidade[index] += 1
		N += 1
		total_obs += 1
	f.close()
	i = 0
	while(i < len(vector)):
		if(vector[i] == None):
			del vector[i]
			del vector_quantidade[i]
			i = 0
		i = i + 1

	return vector, vector_quantidade, N, total_obs, vector_latlong, len(vector)
