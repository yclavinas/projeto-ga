#!/usr/bin/env python

import array
import random
import sys
from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import math
import time
import random

arq_entrada = '../filtro_terremoto_terra.txt'
name = arq_entrada
t_abertura = 'r'

#@profile
def tabelaFatorial():
    i = 0
    vetor = [0] * 100
    f = open("tabela_fatorial.txt", "r")
    for line in f:
        data = str.split(line)
        vetor[i] = data[1]
        i += 1
    f.close()
    return vetor
    
#@profile
# def calc_lat(nome, t_abertura):
#     #abre arq
#     f = open(nome, t_abertura)
#     #x=400, y = 77398

#     menor_lat = str(370)
#     maior_lat = str(0.0)

#     limit_inf = str(34.8)
#     limit_sup = str(36.3)

#     for line in f:
#         data = str.split(line)
#         if(data[6] > maior_lat):
#             if(data[6] >= limit_sup):
#                 maior_lat = data[6]

#     f.seek(0,0)

#     for line in f:
#         data = str.split(line) 
#         if(data[6] < menor_lat):
#             if(data[6] >= limit_inf):
#                 menor_lat = data[6]
      
#     f.close()

#     return maior_lat, menor_lat

# #@profile
# def calc_long(nome, t_abertura):
#     f = open(nome, t_abertura)
#     #x=400, y = 77398

#     menor_long = str(370)
#     maior_long = str(0.0)

#     limit_inf = str(138.8)
#     limit_sup = str(140.3)

#     for line in f:
#         data = str.split(line)
#         if(data[7] > maior_long):
#             if(data[7] >= limit_sup):
#                 maior_long = data[7]

#     f.seek(0,0)

#     for line in f:
#         data = str.split(line) 
#         if(data[7] < menor_long):
#             if(data[7] >= limit_inf):
#                 menor_long = data[7]
    
#     f.close()
#     return maior_long, menor_long

# maior_lat, menor_lat = calc_lat(name, t_abertura)
# maior_long, menor_long = calc_long(name, t_abertura)

menor_long, menor_lat = 138.8, 34.8

#@profile
def calc_grupo_coord(obs_long, obs_lat, menor_lat, menor_long):

    intervalo = 0.1/3
    k, l, index = 0, 0, 0

    #long
    for i in range(0, 150000000, 3333333):
        index = float(i)/100000000 + 138.8
        if(obs_long >= index and obs_long < (index + intervalo)):
            if(index + intervalo > 140.3):
                k -= 1
            break
        k += 1
    for j in range(0, 150000000, 3333333):
        index = float(j)/100000000 + 34.8
        if(obs_lat >= index and obs_lat < (index + intervalo)):
            if(index + intervalo > 36.3):
                l -= 1
            break
        l += 1
    index = k*45 + l

    return int(index)

#@profile
def cria_vector(total_size, nome, t_abertura, menor_lat, menor_long, ano):
    f = open(nome, t_abertura)

    N = 0

    vector_quantidade = [0]*(total_size)
    # kanto region
    for line in f:
        aux2 = str.split(str(line))
        if(int(aux2[0]) == int(ano)):
            if(float(aux2[9]) >= 2.5):
                if(float(aux2[7]) >= 138.8):
                    if(float(aux2[7]) <= 140.3):
                        obs_long = float(aux2[7])
                        if(float(aux2[6]) >= 34.8):
                            if(float(aux2[6]) <= 36.3):
                                obs_lat = float(aux2[6])
                                index = calc_grupo_coord(obs_long, obs_lat, menor_lat, menor_long)
                                if(index < 0 or index > 2024):
                                    print "Deu erro!!!"
                                    exit(0)
                                vector_quantidade[index] += 1             
        N += 1
    print vector_quantidade
    f.close()
    return vector_quantidade, N, sum(vector_quantidade)

#@profile
def calcular_expectations(modified_quant_por_grupo, total_size, N):

    expectations = [0.0] * (total_size)
    for l in xrange(total_size):
        expectations[l] = (float(modified_quant_por_grupo[l])/float(N))
    return expectations

#@profile
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

#@profile
def dados_observados_R(ano):
    
    global menor_lat, menor_long
    menor_lat = float(menor_lat)
    menor_long = float(menor_long)
    total_size = 2025

    quant_por_grupo, N, N_ano = cria_vector(total_size, arq_entrada, 'r', menor_lat, menor_long, ano)
    expectations = calcular_expectations(quant_por_grupo, total_size, N)

    joint_log_likelihood, joint_log_likelihood_NaoUso, descarta_Modelo = log_likelihood(total_size, quant_por_grupo, expectations)

    return joint_log_likelihood, total_size, menor_lat, menor_long, expectations, N_ano, N

#@profile
def log_likelihood(total_size, quant_por_grupo, expectation):

    log_likelihood =  [0]*(total_size)
    joint_log_likelihood = long(0)
    descarta_Modelo = False

    for i in range(total_size):
        if expectation[i] == 0:
            expectation[i] += 1
        # if (quant_por_grupo[i] == 0 and expectation[i] == 0):
        #   log_likelihood[i] += 1      
        # elif (quant_por_grupo[i] != 0 and expectation[i] == 0):
        #   log_likelihood[i] = Decimal('-Infinity')
        #   descarta_Modelo = True
        # else:
            # log_likelihood[i] = -expectation[i] + (quant_por_grupo[i]*math.log10(expectation[i])) - (math.log10(fat(quant_por_grupo[i])))
        if(quant_por_grupo[i] > 100):
            cast = 99
        else:
            cast = quant_por_grupo[i] - 1
        log_likelihood[i] = -expectation[i] + (quant_por_grupo[i]*math.log10(expectation[i])) - (math.log10(float(fatorial[cast])))

    #calcula o joint_log_likelihood
    joint_log_likelihood = sum(log_likelihood)

    return log_likelihood, joint_log_likelihood, descarta_Modelo

total_size = 2025
global mi
mi = 0.0 
global quant_por_grupo
quant_por_grupo = [0] * total_size
global fatorial
fatorial = tabelaFatorial()



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.random)
# Structure initializers

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, total_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#@profile
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


#@profile
def main():
    # random.seed(64)
    CXPB, MUTPB, NGEN = 0.9, 0.1, 100
    ano = 2010
    
    joint_log_likelihood, total_size, menor_lat, menor_long, expectations, N_ano, N = dados_observados_R(ano)
 
    global mi
    mi = float(N_ano)/float(N)
    pop = toolbox.population(n=500)
    
    # fitnesses = list(map(toolbox.evaluate, pop))
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    
    while(ano <= 2010):
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

        ano += 1

        if(ano <= 2010):
            joint_log_likelihood, total_size, menor_lat, menor_long, expectations, N_ano, N = dados_observados_R(ano)
        global mi
        mi = float(N_ano)/float(N)
        
        pop = toolbox.population(n=50)
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        best_ind = tools.selBest(pop, 1)[0]
        for i in range(len(best_ind)):
            global quant_por_grupo
            quant_por_grupo[i] = poisson_press(best_ind[i], mi) - 1 
 
        print quant_por_grupo
        # while True:
        #     try:            
        #         f = open(sys.argv[1], "a")
        #         flock(f, LOCK_EX | LOCK_NB)
        #         f.write(str(ano - 1))
        #         f.write('\n')
        #         for i in range(len((pop, 1)[0])):            
        #             f.write(str((pop, 1)[0][i].fitness.values))
        #         f.write('\n')
        #         global quant_por_grupo
        #         f.write(str(quant_por_grupo))
        #         f.write('\n')
        #         f.write(str(best_ind.fitness.values))
        #         f.write('\n')
        #         flock(f, LOCK_UN)
        #         f.write('\n')
        #     except IOError:
        #         time.sleep(5)
        #         continue
        #     break

        


if __name__ == "__main__":
    main()