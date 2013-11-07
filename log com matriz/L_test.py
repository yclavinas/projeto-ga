from log_likelihood import *
from criar_random import *
import math

joint, descarta_Modelo = log_likelihood(0.5, 'jma_cat_2000_2012_Mth2.5_formatted.dat')
# joint, descarta_Modelo = log_likelihood(0.5, 'testes_7.3.igual.dat')
joint_random = [0.0]*4
descarta_Modelo = [None]*4 
joint_random[0], descarta_Modelo[0] = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[1], descarta_Modelo[1] = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[2], descarta_Modelo[2] = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[3], descarta_Modelo[3] = log_likelihood(0.1, 'testes_7.diferentes.dat')

for i in range(4):
	if descarta_Modelo[i] == True:
		#descarte modelo
		print i
		joint_random[i] = 0

sum_joint = sum(joint_random)

quantile_score = [0.0]*4

for i in range(4):
	quantile_score[i] = (math.fabs(joint_random[i] - joint))/(math.fabs(sum_joint))

quantile_score_mean = (sum(quantile_score))/4

print quantile_score, quantile_score_mean