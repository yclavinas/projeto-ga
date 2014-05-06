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

toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)

toolbox.register("select", tools.selRoulette)



def main():
    # random.seed(64)

    pop = toolbox.population(n=500)
    CXPB, MUTPB, NGEN = 0.9, 0.1, 100
    ano_int = 1997
    ano_str = str(ano_int)
    
    var_coord = 0.5

    while(ano_int <= 2013):
        joint_log_likelihood, total_size, total_obs, menor_lat, menor_long, vector_latlong, expectations, N_ano, N = dados_observados_R(var_coord, ano_str)
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
            selecao = list(map(toolbox.clone, offspring))

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
                for child1, child2 in zip(selecao[::2], selecao[1::2]):
                    if random.random() < CXPB:
                        toolbox.mate(child1, child2)
                        del child1.fitness.values
                        del child2.fitness.values
                        operator1 = 1
                        i = 0
                        while (i < len(selecao)):
                            if (selecao[i] == child1):
                                del selecao[i] 
                                i = i - 1
                            elif (selecao[i] == child2):
                                del selecao[i] 
                                i = i - 1
                            i = i + 1
                    break
                if(operator1 == 0):
                    for mutant in selecao:
                        # if random.random() < MUTPB:
                        toolbox.mutate(mutant, indpb=0.05)
                        del mutant.fitness.values
                        i = 0
                        while (i < len(selecao)):
                            if (selecao[i] == mutant):
                                del selecao[i] 
                                i = i - 1
                            i = i + 1
                        break
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            print("  Evaluated %i individuals" % len(invalid_ind))
            # The population is entirely replaced by the offspring, but the last pop best_ind
            # best_ind = tools.selBest(pop, 1)[0]
            # worst_ind = tools.selWorst(offspring, 1)[0]
            
            # for i in range(len(offspring)):
            #     if (offspring[i] == worst_ind):
            #         offspring[i] = best_ind
            #         break

            pop[:] = offspring        
            CXPB, MUTPB = CXPB - (0.003), MUTPB + (0.003    )
            print MUTPB, CXPB
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