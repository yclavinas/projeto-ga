import math

def L_test(joint_log_likelihood, joint_log_likelihood_simulacao, s):

	L_test = [0] * s
	joint_L_test = [0] * s
	sum_joint_simulacao = sum(joint_log_likelihood_simulacao)

	for i in range(s):
		for j in range(s):
			L_test[j] = (math.fabs(joint_log_likelihood_simulacao[i] - joint_log_likelihood[j]))/(math.fabs(sum_joint_simulacao))
		joint_L_test[i] = sum(L_test)

	return L_test
	# return ((sum(joint_L_test))/s)

def L_test_semS(joint_log_likelihood, joint_log_likelihood_simulacao):
	L_test = (math.fabs(joint_log_likelihood_simulacao - joint_log_likelihood))/(math.fabs(joint_log_likelihood_simulacao))

	return (L_test)

def L_test_sem_correct(joint_log_likelihood, joint_log_likelihood_simulacao, joint_log_likelihood_ind):

	soma = 0
	for i in range(len(joint_log_likelihood_ind)):
		if (joint_log_likelihood_ind[i] <= joint_log_likelihood):
			soma = joint_log_likelihood_ind[i] + soma
	# print type(soma), type(sum(joint_log_likelihood))
	L_test = soma/sum(joint_log_likelihood)
	# print L_test
	# exit(0)
	return (L_test)

