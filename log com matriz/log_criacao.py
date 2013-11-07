from cria_matriz import abre_arq

def log_criacao(matriz, expetations, total_obs, quant_por_grupo, log_likelihood, joint_log_likelihood, arq_entrada, var_coord):
	data = str.split(arq_entrada)

	arq_saida = "log_" + arq_entrada
	f = abre_arq(arq_saida, 'a')

	f.write(arq_saida)
	f.write('\n')

	f.write("matriz :")
	f.write("\n")
	f.writelines(str(matriz))
	f.write("\n")

	f.write("expetations :")
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

	f.write("log_likelihood: ")
	f.write("\n")
	f.write(str(log_likelihood))
	f.write("\n")

	f.write("joint_log_likelihood: ")
	f.write("\n")
	f.write(str(joint_log_likelihood))
	f.write("\n")

	f.write("var_coord: ")
	f.write("\n")
	f.write(str(var_coord))
	f.write("\n")
	f.write("\n")
	f.write("\n")

	f.close()