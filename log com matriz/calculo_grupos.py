def calc_coordenadas(var_coord, name, t_abertura):
	
	from calc_lat import calc_lat
	from calc_longitude import calc_long	

	maior_lat, menor_lat = calc_lat(name, t_abertura)
	maior_long, menor_long = calc_long(name, t_abertura)

	espaco_lat = float(maior_lat) - float(menor_lat)
	espaco_long = float(maior_long) - float(menor_long)

	bins_lat = espaco_lat/var_coord 
	bins_long = espaco_long/var_coord

	bins_lat = round(bins_lat + 1)
	bins_long = round(bins_long + 1)

	return menor_lat, menor_long, bins_lat, bins_long

def calc_grupo_coord(line, menor_lat, menor_long, var_coord):

	i = long(0)
	
	aux2 = str.split(str(line))
	
	obs_menor_long = float(aux2[0])
	obs_menor_lat = float(aux2[1])
	
	dif_lat = obs_menor_lat - menor_lat
	dif_long = obs_menor_long - menor_long

	qual_bin_lat = dif_lat / var_coord
	qual_bin_long = dif_long / var_coord

	return qual_bin_lat, qual_bin_long


