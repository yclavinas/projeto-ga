import random
import sys
import math
import array
import time

from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB

from numpy import pi, zeros, linspace
from ctypes import cdll
import ctypes as ct

k = int(sys.argv[5])
# print k
# print 'now function ',k

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,))


toolbox = base.Toolbox()

###--Para binary com F6--###
# creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)
# INT_MIN, INT_MAX = 0, 1
# toolbox.register("attr_bool", random.randint, INT_MIN, INT_MAX)
# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=44)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# parte1 = 22 *[0]
# parte2 = 22 *[0]


# def evalOneMax(individual):
#     valor1, valor2 = 0, 0
#     for i in range(len(parte1)):
#         # parte1[i] = individual[i]
#         valor1 = valor1 + int((math.pow(2,i))*(individual[21-i]))
#     for i in range(len(parte1)):
#         # parte2[i] = individual[i+22]
#         valor2 = valor2 + int((math.pow(2,i))*(individual[43-i]))

#     # valor1, valor2 = 165377, 2270139

#     valor1 = valor1 * 0.00004768372718899898
#     valor2 = valor2 * 0.00004768372718899898
    
#     valor1 = valor1 - 100
#     valor2 = valor2 - 100

#     x = valor1
#     y = valor2

#     # x, y = -92.11420824866492, 8.248688757106959

#     dentro_raiz = math.pow(x,2) + math.pow(y,2)
#     raiz = math.sqrt(dentro_raiz)
#     seno = math.sin(raiz)
#     seno_pow = math.pow(seno, 2)

#     dividido = 1 + 0.0001*(math.pow(math.pow(x,2) + math.pow(y,2), 2))

#     f6 = (1 - seno_pow/dividido)
#     return f6,

###--Para x, y com F6--###
# creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)
# N_CYCLES = 1

# toolbox.register("attr_flt", random.random)
# toolbox.register("individual", tools.initCycle, creator.Individual,(toolbox.attr_flt, toolbox.attr_flt), n=N_CYCLES)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# def evalOneMax(individual):
#     x = individual[0]
#     y = individual[1]

#     dentro_raiz = math.pow(x,2) + math.pow(y,2)
#     raiz = math.sqrt(dentro_raiz)
#     seno = math.sin(raiz)
#     seno_pow = math.pow(seno, 2)

#     dividido = 1 + 0.0001*(math.pow(math.pow(x,2) + math.pow(y,2), 2))

#     f6 = (1 - seno_pow/dividido)
#     return f6,

###--Para funcoes compostas do cec--###

creator.create("Individual", list, fitness=creator.FitnessMax)

LIMIT_INF, LIMIT_SUP = -100, 100
toolbox.register("attr_float", random.uniform, LIMIT_INF, LIMIT_SUP)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n = 20)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

tf = cdll.LoadLibrary('./test_func.so')

tf.test_func.argtypes=[ct.POINTER(ct.c_double),ct.POINTER(ct.c_double),ct.c_int,ct.c_int,ct.c_int]

tf.test_func.restype=None

n=10; m=2; h=180
xlim=[-27.,-17.]; ylim=[7.,17.];
xwidth=xlim[1]-xlim[0]; ywidth=ylim[1]-ylim[0];
dx=xwidth/(m-1.); dy=ywidth/(h-1.);
x=linspace(xlim[0],xlim[1],m+1)
y=linspace(ylim[0],ylim[1],h+1)



def evalOneMax(individual):
    x = individual[0]
    npdat=zeros(n*m)
    dat = (ct.c_double * len(npdat))()
    for i,val in enumerate(npdat):
        dat[i] = x

    npf=zeros(m)
    f = (ct.c_double * len(npf))()
    for i,val in enumerate(npf):
        f[i] = val 

    r1=tf.test_func(dat,f,ct.c_int(n),ct.c_int(m),ct.c_int(k))

    for pt in f:
        f6 = pt,
    return f6


# print(sys.argv[2], sys.argv[3], sys.argv[4])
# exit(0)

# Operator registering
toolbox.register("evaluate", evalOneMax)
if(int(sys.argv[2]) == 0):
    toolbox.register("mate", tools.cxOnePoint)
elif(int(sys.argv[2]) == 1):
    toolbox.register("mate", tools.cxTwoPoints)
elif(int(sys.argv[2]) == 2):
    toolbox.register("mate", tools.cxUniform, indpb=0.05)
elif(int(sys.argv[2]) == 3):
# toolbox.register("mate", tools.cxPartialyMatched) #int
# toolbox.register("mate", tools.cxOrdered) #int
# toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.05) #int
    toolbox.register("mate", tools.cxBlend, alpha = 0.5)#float
elif(int(sys.argv[2]) == 4):
    toolbox.register("mate", tools.cxSimulatedBinary, eta = 1)#float
elif(int(sys.argv[2]) == 5):
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta = 1, low = -1, up = 1)#float
# toolbox.register("mate", tools.cxMessyOnePoint)

if(int(sys.argv[3]) == 10):
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
elif(int(sys.argv[3]) == 11):
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)
elif(int(sys.argv[3]) == 12):
    # toolbox.register("mutate", tools.mutUniformInt, indpb=0.5, low=0, up=1)#int
    toolbox.register("mutate", tools.mutPolynomialBounded,indpb=0.5, eta = 1, low = -1, up = 1)#float

if(int(sys.argv[4]) == 23):
    toolbox.register("select", tools.selTournament, tournsize=3)
elif(int(sys.argv[4]) == 24):
    toolbox.register("select", tools.selRoulette)
elif(int(sys.argv[4]) == 25):
# toolbox.register("select", tools.selNSGA2)#multi
# toolbox.register("select", tools.selSPEA2)#multi
    toolbox.register("select", tools.selRandom)
elif(int(sys.argv[4]) == 26):
    toolbox.register("select", tools.selBest)
elif(int(sys.argv[4]) == 27):
    toolbox.register("select", tools.selWorst)


def main():
    # random.seed(64)
    
    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.65, 0.08, 100
    # print("Start of evolution")
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    # print("  Evaluated %i individuals" % len(pop))
    
    # Begin the evolution
    evaluations = 0
    j = 0
    for g in range(NGEN):
    
    # while (evaluations < 4000):
        # print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # print("  Evaluated %i individuals" % len(invalid_ind))
        # The population is entirely replaced by the offspring
        best_ind = tools.selBest(pop, 1)[0]
        worst_ind = tools.selWorst(offspring, 1)[0]

        for i in range(len(offspring)):
            if (offspring[i] == worst_ind):
                offspring[i] = best_ind
                break

        pop[:] = offspring 
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length

        j = j + 1

    # for i in range(len(pop)):         
    #     print (pop, 1)[0][i].fitness.values

    while True:
        try:            
            f = open(sys.argv[1], "a")
            flock(f, LOCK_EX | LOCK_NB)
            for i in range(len(pop)):            
                f.write(str((pop, 1)[0][i].fitness.values))
            f.write('\n')
            flock(f, LOCK_UN)
        except IOError:
            time.sleep(5)
            continue
        break
    
    best_ind = tools.selBest(pop, 1)[0]
    # print("Best individual is: %s with fitness value:  \n\n" % best_ind)

    # valor1, valor2 = 0, 0
    # for i in range(len(parte1)):
    #     # parte1[i] = individual[i]
    #     valor1 = valor1 + int((math.pow(2,i))*(best_ind[21-i]))
    # for i in range(len(parte1)):
    #     # parte2[i] = individual[i+22]
    #     valor2 = valor2 + int((math.pow(2,i))*(best_ind[43-i]))

    # valor1 = valor1 * 0.00004768372718899898
    # valor2 = valor2 * 0.00004768372718899898
    
    # valor1 = valor1 - 100
    # valor2 = valor2 - 100

    # x = valor1
    # y = valor2

    # print("Best individual is: %s with fitness value: %s \n\n" % ((x,y), best_ind.fitness.values[0]))

    # f = open(sys.argv[1], "a")
    # flock(f, LOCK_EX | LOCK_NB)
    # f.write(str((best_ind[0],best_ind[1])))
    # f.write(' ')
    # f.write(str((best_ind.fitness.values[0])))
    # f.write('\n')
    # flock(f, LOCK_UN)
    f.close()
    # print '\n'
    # for i in range(len(pop)):
    #     print sum(pop[i])
if __name__ == "__main__":
    main()