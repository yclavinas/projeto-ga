import math

def poisson_press(x,mi):
    if(mi <= 0):
        return
    elif(x >= 0):
        if(x < 1):
            l = math.exp(-mi)
            k = 0
            prob = 1
            while(l < prob):
                k = k + 1
                prob = prob * x
            return (k)
    return 1

def poisson_press2(x,mi):
    if(mi <= 0):
        return
    elif(x >= 0):
        if(x < 1):
            l = math.exp(-mi)
            k = 0
            prob = 1
            while(l < prob):
                k = k + 1
                prob = prob * x
            return (k)
    return 1

print poisson_press(0.15, 10)
print poisson_press(0.50, 15)
print poisson_press(0.85, 10)
