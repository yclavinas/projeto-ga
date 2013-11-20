import math

def L_test(joint_log_likelihood, joint_log_likelihood_simulacao, s):

	L_test = [0] * s
	joint_L_test = [0] * s
	sum_joint_simulacao = sum(joint_log_likelihood_simulacao)

	for i in range(s):
		for j in range(s):
			L_test[j] = (math.fabs(joint_log_likelihood_simulacao[i] - joint_log_likelihood[j]))/(math.fabs(sum_joint_simulacao))
		joint_L_test[i] = sum(L_test)

	print 'joint_L_test'
	print ((sum(joint_L_test))/s)
	exit(0)