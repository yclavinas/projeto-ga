from log_likelihood import *
from criar_random import *

joint, descarta_Modelo = log_likelihood(0.5, 'jma_cat_2000_2012_Mth2.5_formatted.dat')
# joint, descarta_Modelo = log_likelihood(0.5, 'testes_7.3.igual.dat')
joint_random = [0.0]*4
joint_random[0], descarta_Modelo1 = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[1], descarta_Modelo2 = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[2], descarta_Modelo3 = log_likelihood(0.1, 'testes_7.diferentes.dat')
joint_random[3], descarta_Modelo4 = log_likelihood(0.1, 'testes_7.diferentes.dat')

sum_joint = sum(joint_random)

quantile_score = [0.0]*4

for i in range(4):
	quantile_score[i] = (joint_random[i] - joint)/sum_joint

print quantile_score