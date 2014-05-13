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

global mi
mi = 0.0 
global quant_por_grupo

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.random)
# Structure initializers
total_size = 2025
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

    return log_likelihood_total,

# Operator registering
toolbox.register("evaluate", evalOneMax)

toolbox.register("mate", tools.cxTwoPoints)

toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

toolbox.register("select", tools.selRoulette)



def main():
    # random.seed(64)

    CXPB, MUTPB, NGEN = 0.9, 0.1, 100
    ano_int = 1997
    ano_str = str(ano_int)
    
    var_coord = 0.5
    joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N = dados_observados_R(var_coord, ano_str)
    global mi
    mi = float(N_ano)/float(N)
    pop = toolbox.population(n=500)

    while(ano_int <= 2013):
        global mi
        mi = float(N_ano)/float(N)
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
            m = 0
            while (m < 50):
                operator1 = 0
                ja_fez = 0
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < CXPB and ja_fez == 0:
                        toolbox.mate(child1, child2)
                        del child1.fitness.values
                        del child2.fitness.values
                        operator1 = 1
                        m += 2
                        ja_fez = 1
                for mutant in offspring:
                    if(operator1 == 0):
                        if random.random() < MUTPB and ja_fez == 0:
                            toolbox.mutate(mutant, indpb=0.05)
                            del mutant.fitness.values
                            m += 1
                            ja_fez = 1
        # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            print("  Evaluated %i individuals" % len(invalid_ind))
            pop[:] = offspring        
            CXPB, MUTPB = CXPB - (0.003), MUTPB + (0.003)
            # fim loop GERACAO
            joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N = dados_observados_R(var_coord, ano_str)
            global mi
            mi = float(N_ano)/float(N)
            
            pop = toolbox.population(n=100)
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
                f.write(str(ano_int))
                f.write('\n')
                for i in range(len(pop)):            
                    f.write(str((pop, 1)[0][i].fitness.values))
                f.write('\n')
                global quant_por_grupo
                f.write(str(quant_por_grupo))
                f.write('\n')
                f.write(str(best_ind.fitness.values))
                f.write('\n')
                flock(f, LOCK_UN)
            except IOError:
                time.sleep(5)
                continue
            break
        CXPB, MUTPB = 0.9, 0.1
        ano_int += 1
        ano_str = str(ano_int)
if __name__ == "__main__":
    main()  