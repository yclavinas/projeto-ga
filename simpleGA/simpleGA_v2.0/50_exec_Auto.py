#!/usr/bin/env python


import os, time
for w in range(1):
	k = 21 + w
	# print k

	for i in range(1):
		NUM_PROCESSES = 1

		childrenBlend = []

		j = 0
		t = time.time()
		for process in range(NUM_PROCESSES):
		    pid = os.fork() 

		    if pid:
		        childrenBlend.append(pid)

		    else:
		        os.execlp('python', 'python', 'AutoAdaptativo.py', "AA-analise_operadores(cxUniform, selRoulette).txt", str(2), str(11),str(24), str(k))# overlay program
		        assert False, 'error starting program'   
		        os._exit(0)
		    j += 1
		for i, childBlend in enumerate(childrenBlend):
		    os.waitpid(childBlend, 0)
