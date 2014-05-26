def fat(n):

	resultado = 1

	lista = range(1,n+1)

	for x in lista:
		resultado = x * resultado

	return resultado

def tabela_fatorial(n):

	resultado = 1

	f = open("tabela_fatorial.txt", "r")
	for line in f: 
		data = str.split(line)
		if(int(data[0]) == n):
			return int(data[1])
	return int(data[1])
	f.close()
