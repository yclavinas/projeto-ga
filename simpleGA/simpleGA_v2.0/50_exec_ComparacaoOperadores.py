#!/usr/bin/env python

import os, time
for w in range(1):
	k = 21 + w
	print k

	# for i in range(50):
	# 	NUM_PROCESSES = 1

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py',"../../../../../../Dropbox/operadores/" + str(w+1) + "-cxOnePoint(selWorst, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)

	# for i in range(50):
	# 	NUM_PROCESSES = 1

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "../../../../../../Dropbox/operadores/" + str(w+1) + "-cxTwoPoints(selWorst, mutShuffleIndexes).txt", str(1), str(11),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(50):
	# 	NUM_PROCESSES = 1
	#  	childrenBlend = []

	#  	j = 0
	#  	t = time.time()
	#  	for process in range(NUM_PROCESSES):
	#  	    pid = os.fork() 

	#  	    if pid:
	#  	        childrenBlend.append(pid)

	#  	    else:
	#  	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/cxUniform(selRoulette, mutPolynomialBounded).txt", str(2), str(12),str(24), str(k)) # overlay program
	#  	        assert False, 'error starting program'   
	#  	        os._exit(0)
	#  	    j += 1
	#  	for i, childBlend in enumerate(childrenBlend):
	#  	    os.waitpid(childBlend, 0)


	# for i in range(50):
	#  	NUM_PROCESSES = 1
	#  	def timeConsumingFunction():
	#  	    x = 1
	#  	    for n in xrange(1000000):
	#  	        x += 1

	#  	childrenBlend = []

	#  	j = 0
	#  	t = time.time()
	#  	for process in range(NUM_PROCESSES):
	#  	    pid = os.fork() 

	#  	    if pid:
	#  	        childrenBlend.append(pid)

	#  	    else:
	#  	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/cxBlend(selRoulette, mutPolynomialBounded).txt", str(3), str(12),str(24), str(k)) # overlay program
	#  	        assert False, 'error starting program'   
	#  	        os._exit(0)
	#  	    j += 1
	#  	for i, childBlend in enumerate(childrenBlend):
	#  	    os.waitpid(childBlend, 0)


	# for i in range(50):
	#  	NUM_PROCESSES = 1
	#  	def timeConsumingFunction():
	#  	    x = 1
	#  	    for n in xrange(1000000):
	#  	        x += 1

	#  	childrenBlend = []

	#  	j = 0
	#  	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/cxSimulatedBinary(selRoulette, mutPolynomialBounded).txt", str(4), str(12),str(24), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(50):
	# 	NUM_PROCESSES = 1
	# 	def timeConsumingFunction():
	# 	    x = 1
	# 	    for n in xrange(1000000):
	# 	        x += 1

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/cxSimulatedBinaryBounded(selRoulette, mutPolynomialBounded).txt", str(5), str(12),str(24), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(50):

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "../../../../../../Dropbox/operadores/" + str(w+1) + "-mutFlipBit(selWorst, cxOnePoint).txt", str(0), str(10),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(50):

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', "../../../../../../Dropbox/operadores/" + str(w+1) + "-mutPolynomialBounded(selWorst, cxOnePoint).txt", str(0), str(12),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
		#     j += 1
		# for i, childBlend in enumerate(childrenBlend):
		#     os.waitpid(childBlend, 0)


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
		        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/selTournament(cxUniform, mutPolynomialBounded).txt", str(2), str(12),str(23), str(k)) # overlay program
		        assert False, 'error starting program'   
		        os._exit(0)
		    j += 1
		for i, childBlend in enumerate(childrenBlend):
		    os.waitpid(childBlend, 0)


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
		        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/selRoulette(cxOnePoint, mutPolynomialBounded).txt", str(2), str(12),str(24), str(k)) # overlay program
		        assert False, 'error starting program'   
		        os._exit(0)
		    j += 1
		for i, childBlend in enumerate(childrenBlend):
		    os.waitpid(childBlend, 0)


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
		        os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/selRandom(cxOnePoint, mutPolynomialBounded).txt", str(2), str(12),str(25), str(k)) # overlay program
		        assert False, 'error starting program'   
		        os._exit(0)
		    j += 1
		for i, childBlend in enumerate(childrenBlend):
		    os.waitpid(childBlend, 0)


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
				os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/selWorst(cxOnePoint, mutPolynomialBounded).txt", str(2), str(12),str(27), str(k))# overlay program
				assert False, 'error starting program'   
				os._exit(0)
			j += 1
		for i, childBlend in enumerate(childrenBlend):
			os.waitpid(childBlend, 0)

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
				os.execlp('python', 'python', 'simpleGA_V2.0.py', "analiseOperadores/selBest(cxOnePoint, mutPolynomialBounded).txt", str(2), str(12),str(26), str(k))# overlay program
				assert False, 'error starting program'   
				os._exit(0)
			j += 1
		for i, childBlend in enumerate(childrenBlend):
			os.waitpid(childBlend, 0)
