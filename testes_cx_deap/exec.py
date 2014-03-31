import os, time
# for w in range(6):
# 	k = 23 + w

# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py',"CF0" + str(w+3) + "-cxOnePoint(selBest, mutShuffleIndexes).txt", str(0), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)

# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-cxTwoPoints(selBest, mutShuffleIndexes).txt", str(1), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-cxUniform(selBest, mutShuffleIndexes).txt", str(2), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-cxBlend(selBest, mutFlmutShuffleIndexesipBit).txt", str(3), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-cxSimulatedBinary(selBest, mutShuffleIndexes).txt", str(4), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-cxSimulatedBinaryBounded(selBest, mutShuffleIndexes).txt", str(5), str(11),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-mutFlipBit(selBest, cxOnePoint).txt", str(0), str(10),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-mutPolynomialBounded(selBest, cxOnePoint).txt", str(0), str(12),str(26), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-selTournament(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(23), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-selRoulette(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(24), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-selRandom(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(25), str(k)) # overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)


# 	for i in range(2):
# 		NUM_PROCESSES = 500
# 		# def timeConsumingFunction():
# 		#     x = 1
# 		#     for n in xrange(1000000):
# 		#         x += 1

# 		childrenBlend = []

# 		j = 0
# 		t = time.time()
# 		for process in range(NUM_PROCESSES):
# 		    pid = os.fork() 

# 		    if pid:
# 		        childrenBlend.append(pid)

# 		    else:
# 		        os.execlp('python', 'python', 'analise_operadores.py', "CF0" + str(w+3) + "-selWorst(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k))# overlay program
# 		        assert False, 'error starting program'   
# 		        os._exit(0)
# 		    j += 1
# 		for i, childBlend in enumerate(childrenBlend):
# 		    os.waitpid(childBlend, 0)

#cf01
k = 21
for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py',"CF01-cxOnePoint(selBest, mutShuffleIndexes).txt", str(0), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)

for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-cxTwoPoints(selBest, mutShuffleIndexes).txt", str(1), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-cxUniform(selBest, mutShuffleIndexes).txt", str(2), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-cxBlend(selBest, mutFlmutShuffleIndexesipBit).txt", str(3), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-cxSimulatedBinary(selBest, mutShuffleIndexes).txt", str(4), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-cxSimulatedBinaryBounded(selBest, mutShuffleIndexes).txt", str(5), str(11),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-mutFlipBit(selBest, cxOnePoint).txt", str(0), str(10),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-mutPolynomialBounded(selBest, cxOnePoint).txt", str(0), str(12),str(26), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-selTournament(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(23), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-selRoulette(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(24), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-selRandom(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(25), str(k)) # overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)


for i in range(2):
	NUM_PROCESSES = 500
	# def timeConsumingFunction():
	#     x = 1
	#     for n in xrange(1000000):
	#         x += 1

	childrenBlend = []

	j = 0
	t = time.time()
	for process in range(NUM_PROCESSES):
	    pid = os.fork() 

	    if pid:
	        childrenBlend.append(pid)

	    else:
	        os.execlp('python', 'python', 'analise_operadores.py', "CF01-selWorst(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k))# overlay program
	        assert False, 'error starting program'   
	        os._exit(0)
	    j += 1
	for i, childBlend in enumerate(childrenBlend):
	    os.waitpid(childBlend, 0)
