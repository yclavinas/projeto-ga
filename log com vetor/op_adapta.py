import array
import random
import sys
from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from log_likelihood import *
from L_test import *
import math
import time
from calculo_grupos import calc_qual_coord, calc_coordenadas


var_coord = 0.5

joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations = dados_observados_R(var_coord)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.random)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, total_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    quant_por_grupo = [0] * len(individual)
    for i in range(len(individual)):
        if(individual[i] < 0):
            individual[i] = -individual[i]
        quant_por_grupo[i] = int(individual[i] * total_obs)

    log_likelihood_ind, log_likelihood_total, descarta_modelo = log_likelihood(total_size, quant_por_grupo, individual)

    L_test = L_test_sem_correct(joint_log_likelihood, log_likelihood_total, log_likelihood_ind)
    return L_test,

# Operator registering
toolbox.register("evaluate", evalOneMax)
if(int(sys.argv[2]) == 0):
    toolbox.register("mate", tools.cxOnePoint)
elif(int(sys.argv[2]) == 1):
    toolbox.register("mate", tools.cxTwoPoints)
elif(int(sys.argv[2]) == 2):
    toolbox.register("mate", tools.cxUniform, indpb=0.05)
elif(int(sys.argv[2]) == 3):
    toolbox.register("mate", tools.cxBlend, alpha = 0.5)#float
elif(int(sys.argv[2]) == 4):
    toolbox.register("mate", tools.cxSimulatedBinary, eta = 1)#float
elif(int(sys.argv[2]) == 5):
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta = 1, low = -1, up = 1)#float

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
    toolbox.register("select", tools.selRandom)
elif(int(sys.argv[4]) == 26):
    toolbox.register("select", tools.selBest)
elif(int(sys.argv[4]) == 27):
    toolbox.register("select", tools.selWorst)



def main():
    # random.seed(64)

    pop = toolbox.population(n=10)
    CXPB, MUTPB, NGEN = 0.9, 0.1, 100
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    # Begin the evolutionck())
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        # Apply crossover and mutation on the offspring
        m = 50
        while (m > 0):
            operator1 = 0
            m = m - 1
            for child1, child2 in zip(offspring[::50-m], offspring[1::50-m]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
                    operator1 = 1
                break
            if(operator1 == 0):
                for mutant in offspring:
                    # if random.random() < MUTPB:
                    toolbox.mutate(mutant, indpb=0.05)
                    del mutant.fitness.values
                    break
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        # The population is entirely replaced by the offspring, but the last pop best_ind

        best_ind = tools.selBest(pop, 1)[0]
        worst_ind = tools.selWorst(offspring, 1)[0]
        
        for i in range(len(offspring)):
            if (offspring[i] == worst_ind):
                offspring[i] = best_ind
                break

        pop[:] = offspring        
        MUTPB, NGEN = MUTPB + 0.3, NGEN - 0.3
        
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
if __name__ == "__main__":
    main()  