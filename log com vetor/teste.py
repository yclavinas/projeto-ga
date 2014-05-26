def tabela_fatorial():
	resultado = 1
	n = 300
	f = open("tabela_fatorial.txt", "w")
	resultado = 1

	lista = range(1,n+1)

	for x in lista:
		resultado = x * resultado
		f.write(str(x))
		f.write(str(' '))
		f.write(str(resultado))
		f.write(str('\n'))
	f.close()

if __name__ == "__main__":
    tabela_fatorial()  