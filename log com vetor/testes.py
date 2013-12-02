from log_likelihood import *
from L_test import *

joint_log_likelihood, total_size, total_obs = dados_observados_R()

#fazer a evolucao de GA

#calcular o evolve(?) nao deveria ser fitness?????? com L_test
print joint_log_likelihood
L_test = (L_test_semS (joint_log_likelihood, joint_log_likelihood/10100))
print L_test

L_test = (L_test_semS (joint_log_likelihood, joint_log_likelihood*100000000100))
print L_test

# list1 = ['physics', 'chemistry', 1997, 2000];
# list2 = [1, 2, 3, 4, 5 ];
# list3 = ["a", "b", "c", "d"];

# print "list1[0]: ", list1[0]
# print "list2[1:5]: ", list2[1:5]