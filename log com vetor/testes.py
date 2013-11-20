import random
n = 0
for l in xrange(100000):
		expectations = [None] * (100000)
		expectations[l] = random.random()
		# print expectations[l]
		if (expectations[l] == 0):
			print "tem"
		#total = 100
		n += expectations[l] * 1000

print n