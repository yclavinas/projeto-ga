import os, time
for w in range(1):
	k = 21 + w
	print k

	# for i in range(100):
	# 	NUM_PROCESSES = 1

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'profiler2.0.py',"../Dropbox/operadores-?/" + str(w+1) + "-cxOnePoint(selWorst, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)

	# for i in range(100):
	# 	NUM_PROCESSES = 1

	# 	childrenBlend = []

	# 	j = 0
	# 	t = time.time()
	# 	for process in range(NUM_PROCESSES):
	# 	    pid = os.fork() 

	# 	    if pid:
	# 	        childrenBlend.append(pid)

	# 	    else:
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-cxTwoPoints(selWorst, mutShuffleIndexes).txt", str(1), str(11),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
	# 	NUM_PROCESSES = 1
	#  	childrenBlend = []

	#  	j = 0
	#  	t = time.time()
	#  	for process in range(NUM_PROCESSES):
	#  	    pid = os.fork() 

	#  	    if pid:
	#  	        childrenBlend.append(pid)

	#  	    else:
	#  	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-cxUniform(selWorst, mutShuffleIndexes).txt", str(2), str(11),str(27), str(k)) # overlay program
	#  	        assert False, 'error starting program'   
	#  	        os._exit(0)
	#  	    j += 1
	#  	for i, childBlend in enumerate(childrenBlend):
	#  	    os.waitpid(childBlend, 0)


	for i in range(1):
	 	NUM_PROCESSES = 1
	 	def timeConsumingFunction():
	 	    x = 1
	 	    for n in xrange(1000000):
	 	        x += 1

	 	childrenBlend = []

	 	j = 0
	 	t = time.time()
	 	for process in range(NUM_PROCESSES):
	 	    pid = os.fork() 

	 	    if pid:
	 	        childrenBlend.append(pid)

	 	    else:
	 	        os.execlp('python', 'python', 'simpleGA_V2.0.py', str(w+1) + "-cxBlendComCalc.txt", str(3), str(11),str(27), str(k)) # overlay program
	 	        assert False, 'error starting program'   
	 	        os._exit(0)
	 	    j += 1
	 	for i, childBlend in enumerate(childrenBlend):
	 	    os.waitpid(childBlend, 0)


	# # # for i in range(100):
	# # #  	NUM_PROCESSES = 1
	# # #  	def timeConsumingFunction():
	# # #  	    x = 1
	# # #  	    for n in xrange(1000000):
	# # #  	        x += 1

	# # #  	childrenBlend = []

	# # #  	j = 0
	# # #  	t = time.time()
	# # # 	for process in range(NUM_PROCESSES):
	# # # 	    pid = os.fork() 

	# # # 	    if pid:
	# # # 	        childrenBlend.append(pid)

	# # # 	    else:
	# # # 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-cxSimulatedBinary(selWorst, mutShuffleIndexes).txt", str(4), str(11),str(27), str(k)) # overlay program
	# # # 	        assert False, 'error starting program'   
	# # # 	        os._exit(0)
	# # # 	    j += 1
	# # # 	for i, childBlend in enumerate(childrenBlend):
	# # # 	    os.waitpid(childBlend, 0)


	# # # for i in range(100):
	# # # 	NUM_PROCESSES = 1
	# # # 	def timeConsumingFunction():
	# # # 	    x = 1
	# # # 	    for n in xrange(1000000):
	# # # 	        x += 1

	# # # 	childrenBlend = []

	# # # 	j = 0
	# # # 	t = time.time()
	# # # 	for process in range(NUM_PROCESSES):
	# # # 	    pid = os.fork() 

	# # # 	    if pid:
	# # # 	        childrenBlend.append(pid)

	# # # 	    else:
	# # # 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-cxSimulatedBinaryBounded(selWorst, mutShuffleIndexes).txt", str(5), str(11),str(27), str(k)) # overlay program
	# # # 	        assert False, 'error starting program'   
	# # # 	        os._exit(0)
	# # # 	    j += 1
	# # # 	for i, childBlend in enumerate(childrenBlend):
	# # # 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-mutFlipBit(selWorst, cxOnePoint).txt", str(0), str(10),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-mutPolynomialBounded(selWorst, cxOnePoint).txt", str(0), str(12),str(27), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-selTournament(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(23), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-selRoulette(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(24), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-selRandom(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(25), str(k)) # overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)


	# for i in range(100):
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-selWorst(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(27), str(k))# overlay program
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
	# 	        os.execlp('python', 'python', 'profiler2.0.py', "../Dropbox/operadores-?/" + str(w+1) + "-selBest(cxOnePoint, mutShuffleIndexes).txt", str(0), str(11),str(26), str(k))# overlay program
	# 	        assert False, 'error starting program'   
	# 	        os._exit(0)
	# 	    j += 1
	# 	for i, childBlend in enumerate(childrenBlend):
	# 	    os.waitpid(childBlend, 0)
