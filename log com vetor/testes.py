import os, time

NUM_PROCESSES = 10

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
        # timeConsumingFunction()
        # os.execl('Documents/UnB/Ga/projeto-ga/log com vetor/simple_GA.py', 1)
        # args = ("test","abc")
        # os.execvp('Users/yclavinas/Documents/UnB/Ga/projeto-ga/log com vetor/simple_GA.py', args)
        # os.execvp('simple_GA.py', args)
        os.execlp('python', 'python', 'simple_GA.py', "saida_final_cxBlend"+str(j)+".txt", "blend") # overlay program
        assert False, 'error starting program'   
        os._exit(0)
    j += 1
for i, childBlend in enumerate(childrenBlend):
    os.waitpid(childBlend, 0)

childrentwopoints = []
j = 0
t = time.time()
for process in range(NUM_PROCESSES):
    pid = os.fork() 

    if pid:
        childrentwopoints.append(pid)
    else:
        # timeConsumingFunction()
        # os.execl('Documents/UnB/Ga/projeto-ga/log com vetor/simple_GA.py', 1)
        # args = ("test","abc")
        # os.execvp('Users/yclavinas/Documents/UnB/Ga/projeto-ga/log com vetor/simple_GA.py', args)
        # os.execvp('simple_GA.py', args)
        os.execlp('python', 'python', 'simple_GA.py', "saida_final_twopoints"+str(j)+".txt", "twopoints") # overlay program
        assert False, 'error starting program'   
        os._exit(0)
    j += 1
for i, childtwopoints in enumerate(childrentwopoints):
    os.waitpid(childtwopoints, 0)

