
import array
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from log_likelihood import *
from L_test import *

joint_log_likelihood, total_size, total_obs = dados_observados_R()

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
        quant_por_grupo[i] = int(individual[i] * (total_obs/1000))

    log_likelihood_ind = log_likelihood(total_size, quant_por_grupo, individual)

    L_test = L_test_semS(joint_log_likelihood, log_likelihood_ind[0])
    return L_test,


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)

    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats,
                        halloffame=hof, verbose=True)

    melhor_log_likelihood = 0

    quant_por_grupo = [0] * len(pop[0])
    for i in range(len(pop[0])):
        print i
        quant_por_grupo[i] = int(pop[0][i] * (total_obs/1000))
        log_likelihood_ind = log_likelihood(total_size, quant_por_grupo, pop[0])
        if (log_likelihood_ind > melhor_log_likelihood):
            melhor_log_likelihood = log_likelihood_ind
            best = pop[0]

    L_test_best = L_test_semS(joint_log_likelihood, melhor_log_likelihood[0])


    return pop, stats, hof

if __name__ == "__main__":
    main()