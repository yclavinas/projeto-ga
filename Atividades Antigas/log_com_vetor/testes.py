import math

def poisson_press(x,mi):
    if(mi <= 0):
        print "mi <= 0"
        return
    elif(x >= 0):
        if(x < 1):
            l = math.exp(-mi)
            k = 1
            prob = 1 * x
            while(prob>l):
                k += 1
                prob = prob * x
            return (k)


def main():
	print poisson_press(0.36605219053681026, 0.001512556948)

if __name__ == "__main__":
    main()

