def fat(n):

	resultado = 1

	lista = range(1,n+1)

	for x in lista:
		resultado = x * resultado

	return resultado

def tabela_fatorial(n):
	import math

	resultado = 1
	saida = 0
	f = open("tabela_fatorial.txt", "r")
	for line in f:
		data = str.split(line)
		if(int(data[0]) == n):
			saida = int(data[1])
			break
	f.close()
	saida = int(data[1])
	
	# if(saida == 0):
	# 	print n
	# 	xis = n/math.e
	# 	print xis
	# 	saida = ( math.sqrt(2*math.pi*n) ) * ( math.pow(xis, n) )
	return saida
