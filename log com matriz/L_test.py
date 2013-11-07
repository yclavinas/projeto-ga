from log_likelihood import *
import random

for i in range(10):
	print random.randint(1, 10)


joint1, descarta_Modelo = log_likelihood(0.5, 1)
print joint1, descarta_Modelo
joint2, descarta_Modelo = log_likelihood(0.5, 2)
print joint2, descarta_Modelo

#quantile_score = 