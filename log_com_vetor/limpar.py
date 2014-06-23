#!/usr/bin/python
import re

# phone = "2004-959-559 # This is Phone Number http://www.google.com \n"
# # Delete Python-style comments
# num = re.sub(r'#.*$', "", phone)
# # print "Phone Num : ", num

# # Remove anything other than digits
# num = re.sub(r'\D', "", phone)    
# # print "Phone Num : ", num

# phone = "2004-959-559 # This http://www.google.com is Phone Number http://www.google.com \n"
# text = re.sub(r'http.*', '', phone, flags=re.MULTILINE)
# print text


text = open('saida_final_2points.txt', 'r')
saveFile = open('2points_correto.txt', 'w')

for line in text:

	data = re.sub(r'Tempo total de execucao 1a em segundos:', '\t', line, flags=re.MULTILINE)	
	data = re.sub(r'Best L-test value (0|[1-9][0-9]?)', '\n', data, flags=re.MULTILINE)

	# data = re.sub(r'(Sat Feb|Fri Jan|Thu Jan|Wed Jan|Tue Jan|Mon Jan|Sun Jan|Sat Jan|Mon Jan).*', '', data, flags=re.MULTILINE)
	# #melhorar ne?
	# data = re.sub(r'[a-z]*@[a-z]+mail.com', '', data, flags=re.MULTILINE)
	# data = re.sub(r'sao paulo', 'saoPaulo', data, flags=re.MULTILINE)
	
	saveFile.write(data)
	saveFile.write('\n')

print("End :D")

saveFile.close()
text.close()