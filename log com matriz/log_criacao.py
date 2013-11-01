from cria_vector import abre_arq

def log_criacao(expetations, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, agrupamento):
	arq_saida = "log_" + arq_entrada
	f = abre_arq(arq_saida, 'a')

	f.write(arq_saida)
	f.write('\n')

	f.write("expetations["+str(agrupamento)+"] :")
	f.write("\n")
	f.writelines(str(expetations))
	f.write("\n")

	f.write("total_obs: ")
	f.write("\n")
	f.write(str(total_obs))
	f.write("\n")

	f.write("quant_por_grupo: ")
	f.write("\n")
	f.write(str(quant_por_grupo))
	f.write("\n")

	f.write("log_likelihood["+str(agrupamento)+"]: ")
	f.write("\n")
	f.write(str(log_likelihood))
	f.write("\n")

	f.write("joint_log_likelihood: ")
	f.write("\n")
	f.write(str(joint_log_likelihood))
	f.write("\n")
	f.write("\n")
	f.write("\n")

	f.close()