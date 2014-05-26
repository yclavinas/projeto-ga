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
	f.close()
	if(saida == 0):
		print n
		saida = ( math.sqrt(2*math.pi*n) ) * ( math.pow(n/math.e, n) )
	return saida
