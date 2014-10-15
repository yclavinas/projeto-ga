#!/usr/bin/python
import re

salva = 0
ano = 2006
while(ano <= 2011):
	text = open('AA-analise_operadores(cxUniform, selRoulette).txt', 'r')
	ano_salvar = ano
	saveFile = open(str(ano_salvar)+'-AA-analise_operadores(cxUniform, selRoulette).txt', 'a')
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
		