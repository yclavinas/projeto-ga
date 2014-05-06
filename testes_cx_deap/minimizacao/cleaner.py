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


text = open('CF06-cxBlend(selWorst, mutFlmutShuffleIndexesipBit).txt', 'r')
saveFile = open('CF06/clean_CF06-cxBlend(selWorst, mutFlmutShuffleIndexesipBit).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-cxOnePoint(selWorst, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-cxOnePoint(selWorst, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-cxSimulatedBinary(selWorst, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-cxSimulatedBinary(selWorst, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

# text = open('CF06-cxSimulatedBinaryBounded(selWorst, mutShuffleIndexes).txt', 'r')
# saveFile = open('CF06/clean_CF06-cxSimulatedBinaryBounded(selWorst, mutShuffleIndexes).txt', 'w')

# for line in text:
	
# 	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
# 	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
# 	saveFile.write(data)

text = open('CF06-cxTwoPoints(selWorst, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-cxTwoPoints(selWorst, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-cxUniform(selWorst, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-cxUniform(selWorst, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-mutFlipBit(selWorst, cxOnePoint).txt', 'r')
saveFile = open('CF06/clean_CF06-mutFlipBit(selWorst, cxOnePoint).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

# text = open('CF06-mutPolynomialBounded(selWorst, cxOnePoint).txt', 'r')
# saveFile = open('CF06/clean_CF06-mutPolynomialBounded(selWorst, cxOnePoint).txt', 'w')

# for line in text:
	
# 	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
# 	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-mutShuffleIndexes(selWorst, cxOnePoint).txt', 'r')
saveFile = open('CF06/clean_CF06-mutShuffleIndexes(cxOnePoint, selBest).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-selRandom(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_selRandom(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-selRoulette(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-selRoulette(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-selTournament(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-selTournament(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-selWorst(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-selWorst(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)

text = open('CF06-selBest(cxOnePoint, mutShuffleIndexes).txt', 'r')
saveFile = open('CF06/clean_CF06-selBest(cxOnePoint, mutShuffleIndexes).txt', 'w')

for line in text:
	
	data = re.sub(r'\(', '', line, flags=re.MULTILINE)
	data = re.sub(r',\)', ' ', data, flags=re.MULTILINE)
	
	saveFile.write(data)





print("End :D")

saveFile.close()
text.close()