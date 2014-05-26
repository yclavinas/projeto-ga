def tabela_fatorial():
	resultado = 1
	n = 29
	f = open("tabela_fatorial.txt", "r")
	for line in f: 
		data = str.split(line)
		if(int(data[0]) == n):
			print data[1]
			exit(0)
	print data[1]
	f.close()

if __name__ == "__main__":
    tabela_fatorial()  