import array
import random
import sys


from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from log_likelihood import *
from L_test import *
import math
import time
from calculo_grupos import calc_qual_coord, calc_coordenadas



var_coord = 0.1

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
    # print L_test
    return L_test,

# Operator registering
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutFlipBit)
# toolbox.register("select", tools.selDoubleTournament, parsimony_size = 2, fitness_first = True)
toolbox.register("select", tools.selTournament, tournsize = 3)
# fitness_size


f = open(sys.argv[1], "a")

def main():
    random.seed(64)

    pop = toolbox.population(n=500)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100
    
    # print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    # Begin the evolution
    inicio = (time.clock())
    antigo = inicio
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
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring, but the last pop best_ind

        # f.write(s)
        # f.write('\n\n')
        best_ind = tools.selBest(pop, 1)[0]
        worst_ind = tools.selWorst(offspring, 1)[0]
        
        for i in range(len(offspring)):
            if (offspring[i] == worst_ind):
                offspring[i] = best_ind
                break

        pop[:] = offspring        

        # Gather all the fitnesses in one list and print the stats
        # meio = (time.clock())

        # print(meio - inicio)
        fim = (time.clock())
        
    f.write(str(max(fits)))
    
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()
    print best_ind.fitness.values, best_ind
    print '\n'
    print expectations
if __name__ == "__main__":
    main()  