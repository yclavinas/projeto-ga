def main():

	arq_entrada = 'filtro_terremoto_terra.txt'
	arq_saida = 'quantAnos.txt'

	t_abertura = 'r'
	f = open(arq_entrada, t_abertura)

	N = 0
	N_ano = 0
	total_obs = long(0)
	g = open(arq_saida, 'w')
	ano = 2000

	# kanto region
	while (ano <= 2013):
		for line in f:

			aux2 = str.split(str(line))
			if(int(aux2[0]) == ano):
				if(float(aux2[7]) >= 138.8):
					if(float(aux2[6]) >= 34.8):
						if(float(aux2[9]) > 2.5):
							# print aux2[9], aux2[0], aux2[7], aux2
							# exit(0)
							N_ano += 1 
			N += 1
			total_obs += 1		
		f.close()
		f = open(arq_entrada, t_abertura)
		
		# print(N_ano)
		g.write(str(ano))
		g.write(' ')
		g.write(str(N_ano))
		g.write('\n')
		ano += 1
		N_ano = 0
	g.close()
	
if __name__ == "__main__":
	main()