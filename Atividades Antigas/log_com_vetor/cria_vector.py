def cria_vector(total_size, nome, t_abertura, menor_lat, menor_long, var_coord, ano_str):

	from calculo_grupos import calc_grupo_coord
	import random

	f = open(nome, t_abertura)

	N = 0
	N_ano = 0
	total_obs = long(0)

	vector = [None]*(total_size)
	vector_quantidade = [0]*(total_size)
	vector_latlong = [None]*(total_size)
	# kanto region
	for line in f:

		aux2 = str.split(str(line))
		if(int(aux2[0]) == int(ano_str)):
			if(aux2[7] >= 138.8):
				obs_menor_long = float(aux2[7])
			if(aux2[7] >= 34.8):
				obs_menor_lat = float(aux2[6])

			x_long, y_lat, index = calc_grupo_coord(obs_menor_long, obs_menor_lat, menor_lat, menor_long, var_coord)
					
			vector[index] = line
			vector_quantidade[index] += 1
			N_ano += 1 
		N += 1
		total_obs += 1
	f.close()
	i = 0
	return vector, vector_quantidade, N, total_obs, vector_latlong, len(vector), N_ano
