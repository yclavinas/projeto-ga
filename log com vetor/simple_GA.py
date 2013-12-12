import array
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from log_likelihood import *
from L_test import *
import math
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
        individual[i] = math.fabs(individual[i])
        quant_por_grupo[i] = int(individual[i] * (total_obs/1000))

    log_likelihood_ind = log_likelihood(total_size, quant_por_grupo, individual)

    L_test = L_test_semS(joint_log_likelihood, log_likelihood_ind[0])
    return L_test,

# Operator registering
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxBlend, alpha = 0.6)
toolbox.register("mutate", tools.mutFlipBit)
toolbox.register("select", tools.selDoubleTournament, parsimony_size = 2, fitness_first = True)
# toolbox.register("select", tools.selTournament, tournsize=3)
# fitness_size

arq_saida = "saida_final.txt"
f = open(arq_saida, 'w')

def main():
    # random.seed(64)
    
    pop = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop), len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < MUTPB:
                if(std < 20.00):##tenho que estudar isso!!!
                    indpb=0.05
                elif(std < 200.00):
                    indpb=0.15
                else:
                    indpb=0.45
                toolbox.mutate(mutant, indpb)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring, but the last pop best_ind

        
        selBest = tools.selBest(pop, 1)[0]
        # selBest = toolbox.select(pop, 1, len(pop))[0]
        quant_por_grupo = [0] * len(selBest)
        for j in range(len(selBest)):
            quant_por_grupo[j] = int(selBest[j] * (total_obs/1000))
        log_likelihood_ind = log_likelihood(total_size, quant_por_grupo, selBest)

        L_test_best_evolucao = L_test_semS(joint_log_likelihood, log_likelihood_ind[0])
        s = 'Best L_test of the pop[%d]: ' %     g + str(L_test_best_evolucao)
        print s

        f.write(s)
        f.write('\n\n')

        pop[:] = offspring

        for i in range(len(pop)):
            quant_por_grupo = [0] * len(pop[i])
            for j in range(len(pop[i])):
                quant_por_grupo[j] = int(pop[i][j] * (total_obs/1000))
            log_likelihood_ind = log_likelihood(total_size, quant_por_grupo, pop[i])
            L_test_subs = L_test_semS(joint_log_likelihood, log_likelihood_ind[0])
            if(L_test_subs < L_test_best_evolucao):
               pop[0] = selBest 
               break
        

        # Gather all the fitnesses in one list and print the stats
        

    
    print("-- End of (successful) evolution --")
    
    
    # best_ind = tools.selBest(pop, 1)[0]
    # print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    print "L_test da melhor"
    print L_test_best_evolucao

    f.write("Best L-test value: ")
    f.write(str(L_test_best_evolucao))
    f.write('\n\n')
    #mostrar o melhor
    for i in range(len(selBest)):

        if(vector_latlong[i] == None):
            print 'para tal lat  e long fora dos dados'
            s = str('Latitude and longitude not available, model output: ' + str(selBest[i]))
            f.write(s)
            f.write('\n')
        else:
            print 'para tal lat  e long %s' % vector_latlong[i]
            s = str('Latitude and longitude: ' + str(vector_latlong[i]) + '; model output: ' + str(selBest[i]))
            f.write(s)
            f.write('\n')
        
        print "tal modelo",  
        print selBest[i]
        

    f.close()

if __name__ == "__main__":
    main()  