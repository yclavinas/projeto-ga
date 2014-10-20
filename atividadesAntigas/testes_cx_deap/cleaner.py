#!/usr/bin/python
import re

# phone = "2001-959-559 # This is Phone Number http://www.google.com \n"
# # Delete Python-style comments
# num = re.sub(r'#.*$', "", phone)
# # print "Phone Num : ", num

# # Remove anything other than digits
# num = re.sub(r'\D', "", phone)    
# # print "Phone Num : ", num

# phone = "2001-959-559 # This http://www.google.com is Phone Number http://www.google.com \n"
# text = re.sub(r'http.*', '', phone, flags=re.MULTILINE)
# print text


text = open('CF01/CF01-cxBlend(selBest, mutFlmutShuffleIndexesipBit).txt', 'r')
saveFile = open('CF01/clean_CF01-cxBlend(selBest, mutFlmutShuffleIndexesipBit).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-cxOnePoint(selBest, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-cxOnePoint(selBest, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-cxSimulatedBinary(selBest, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-cxSimulatedBinary(selBest, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-cxSimulatedBinaryBounded(selBest, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-cxSimulatedBinaryBounded(selBest, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-cxTwoPoints(selBest, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-cxTwoPoints(selBest, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-cxUniform(selBest, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-cxUniform(selBest, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-mutFlipBit(selBest, cxOnePoint).txt', 'r')
saveFile = open('CF01/clean_CF01-mutFlipBit(selBest, cxOnePoint).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-mutPolynomialBounded(selBest, cxOnePoint).txt', 'r')
saveFile = open('CF01/clean_CF01-mutPolynomialBounded(selBest, cxOnePoint).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-mutShuffleIndexes(selBest, cxOnePoint).txt', 'r')
saveFile = open('CF01/clean_CF01-mutShuffleIndexes(cxOnePoint, selBest).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-selRandom(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_selRandom(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-selRoulette(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-selRoulette(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-selTournament(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-selTournament(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-selWorst(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-selWorst(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF01/CF01-selBest(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF01/clean_CF01-selBest(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)





print("End :D")

saveFile.close()
text.close()