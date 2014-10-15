#!/usr/bin/python
import re

salva = 0
ano = 2000
while(ano <= 2010):
	text = open('cxUniform(selRoulette, mutPolynomialBounded).txt', 'r')
	ano_salvar = ano
	saveFile = open(str(ano_salvar)+'-cxUniform(selRoulette, mutPolynomialBounded).txt', 'a')
	for line in text:
		# data = re.sub(r'\[.*', '', line, flags=re.MULTILINE)
		data = re.sub(r'\,\)\(', '', line, flags=re.MULTILINE)
		data = re.sub(r'\(-[0-9]*\.[0-9]*\,\)\n', '\n', data, flags=re.MULTILINE)
		data = re.sub(r'\(-.*\n', '', data, flags=re.MULTILINE)
		data = re.sub(r'\[', '', data, flags=re.MULTILINE)
		data = re.sub(r'\]', '', data, flags=re.MULTILINE)
		data = re.sub(r'\,', '', data, flags=re.MULTILINE)
		testes = str.split(data)
		if(len(testes)):
			if(float(testes[0]) == ano):
				salva = 1
			elif(salva == 1):
				salva = 0

				saveFile.write(data)
				saveFile.write('\n')
	ano += 1
		