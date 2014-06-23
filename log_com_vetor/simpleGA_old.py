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
from poisson_press import poisson_press

total_size = 2025
global mi
mi = 0.0 
global quant_por_grupo
quant_por_grupo = [0] * total_size

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.random)
# Structure initializers

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, total_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    global quant_por_grupo
    quant_por_grupo = [0] * len(individual)
    for i in range(len(individual)):
        if(individual[i] < 0):
            individual[i] = -individual[i]
        global quant_por_grupo
        quant_por_grupo[i] = poisson_press(individual[i], mi)

    log_likelihood_ind, log_likelihood_total, descarta_modelo = log_likelihood(total_size, quant_por_grupo, individual)

    # L_test = L_test_sem_correct(joint_log_likelihood, log_likelihood_total, log_likelihood_ind)
    # return L_test,
    return log_likelihood_total,

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
    toolbox.register("mate", tools.cxSimulatedBinary, eta = 0.5)#float
elif(int(sys.argv[2]) == 5):
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta = 0.5, low = -1, up = 1)#float

if(int(sys.argv[3]) == 10):
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
elif(int(sys.argv[3]) == 11):
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
elif(int(sys.argv[3]) == 12):
    # toolbox.register("mutate", tools.mutUniformInt, indpb=0.5, low=0, up=1)#int
    toolbox.register("mutate", tools.mutPolynomialBounded,indpb=0.05, eta = 1, low = -1, up = 1)#float

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
    CXPB, MUTPB, NGEN = 0.9, 0.1, 10
    ano_int = 2000
    ano_str = str(ano_int)
    
    var_coord = 0.5
    joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N = dados_observados_R(var_coord, ano_str)
 
    global mi
    mi = float(N_ano)/float(N)
    pop = toolbox.population(n=5)
    
    # fitnesses = list(map(toolbox.evaluate, pop))
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    
    while(ano_int <= 2010):
        global mi
        mi = float(N_ano)/float(N)
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
            print("Start of evolution")
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant, indpb=0.05)
                    del mutant.fitness.values
        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(toolbox.evaluate, invalid_ind))
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
            # fim loop GERACAO

        ano_int = ano_int + 1
        
        ano_str = str(ano_int)

        joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N = dados_observados_R(var_coord, ano_str)
        global mi
        mi = float(N_ano)/float(N)
        
        pop = toolbox.population(n=5)
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        best_ind = tools.selBest(pop, 1)[0]
        for i in range(len(best_ind)):
            global quant_por_grupo
            quant_por_grupo[i] = poisson_press(best_ind[i], mi)
 

        while True:
            try:            
                f = open(sys.argv[1], "a")
                flock(f, LOCK_EX | LOCK_NB)
                f.write(str(ano_int - 1))
                f.write('\n')
                for i in range(len((pop, 1)[0])):            
                    f.write(str((pop, 1)[0][i].fitness.values))
                f.write('\n')
                global quant_por_grupo
                f.write(str(quant_por_grupo))
                f.write('\n')
                f.write(str(best_ind.fitness.values))
                f.write('\n')
                flock(f, LOCK_UN)
                f.write('\n')
            except IOError:
                time.sleep(5)
                continue
            break
        ano_int = 2010



if __name__ == "__main__":
    main()  