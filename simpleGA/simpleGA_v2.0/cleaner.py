#!/usr/bin/python
import re




text = open('2000 Uniform,roleta,polynomialBounded', 'r')

saveFile = open('teste.txt', 'a')
for line in text:
	data = re.sub(r'^[a-z].*$', '', line, flags=re.MULTILINE)
	# data = re.sub(r'\n', '', line, flags=re.MULTILINE)
	saveFile.write(data)
	saveFile.write('\n')
text = open('teste.txt', 'r')
