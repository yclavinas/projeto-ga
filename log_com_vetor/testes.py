def fat(n):
	resultado = 1
	lista = range(1,n+1)

	for x in lista:
		resultado = x * resultado

	return resultado
	
if __name__ == "__main__":
	print(fat(100000))