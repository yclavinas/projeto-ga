import os, time
for w in range(1):
	k = 21 + w
	print k

	for i in range(50):
		NUM_PROCESSES = 1

		childrenBlend = []

		j = 0
		t = time.time()
		for process in range(NUM_PROCESSES):
		    pid = os.fork() 

		    if pid:
		        childrenBlend.append(pid)

		    else:
		        os.execlp('python', 'python', 'analise_operadores.py', "../../Dropbox/100operadores-cf0?/" + str(w+1) + "-selWorst_COMtabelafatorial(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k))# overlay program
		        assert False, 'error starting program'   
		        os._exit(0)
		    j += 1
		for i, childBlend in enumerate(childrenBlend):
		    os.waitpid(childBlend, 0)
