###
import sys
import random
import math

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def println(self):
        print "(%f, %f)" % (self.x, self.y)

if __name__ == '__main__':
    x = random.random()
    y = x

    p1 = Point(x, y)
    x = 3   
    print (1.0 + 0.001)
    p2 = Point(7, 17)
    p1.println()
    p2.println()
    p1.add(p2).println()
    sys.exit(0)
###