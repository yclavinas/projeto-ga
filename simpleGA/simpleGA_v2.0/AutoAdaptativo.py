#!/usr/bin/env python

import time
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
import numpy

slices = 5
arq_entrada = '../../jmacat_20000101_20131115_Mth2.5.dat'
name = arq_entrada
t_abertura = 'r'
menor_long, menor_lat = 138.8, 34.8
maior_long, maior_lat = 141.05, 37.05
depth = 100.0
mag = 2.5
total_size = 2025
global quant_por_grupo
quant_por_grupo = [0] * total_size
global fatorial
global mi 

#@profile
def calculo_lambda(ano):
    f = open(arq_entrada, 'r')
    lambda_ano = 0.0
    ano_limite = ano + slices
    # kanto region
    while (ano < ano_limite):
        for line in f:
            parTerremoto = str.split(str(line))

            if(int(parTerremoto[2]) == ano):
                obs_long = float(parTerremoto[0])
                obs_lat = float(parTerremoto[1])

                if(obs_long > menor_long and obs_long < maior_long):                    
                    if(obs_lat > menor_lat and obs_lat < maior_lat):
                        if(float(parTerremoto[6]) <= depth):
                            if(float(parTerremoto[5]) >= mag):
                                lambda_ano +=1
        f.seek(0,0)
        ano +=1
    lambda_ano = lambda_ano/total_size
    return lambda_ano

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


fatorial = tabelaFatorial()
#@profile
def calc_grupo_coord(obs_long, obs_lat, menor_lat, menor_long):

    
    k, l, index = 0, 0, 0

    #100000000 valor utilizado para melhorar a precisao, por ser fracao indeterminada, 1/3
    max_range_long = (maior_long - menor_long)*100000000#2.25
    max_range_lat = (maior_lat - menor_lat)*100000000
    
    end_range_long = max_range_long/45#0.05
    end_range_lat = max_range_lat/45

    intervalo = (maior_long - menor_long)/45

    for i in range(0, int(max_range_long), int(end_range_long)):
        #Viu? Tirei o 100000000 que eu havia multiplicado
        index = float(i)/100000000 + menor_long
        if(obs_long >= index and obs_long < (index + intervalo)):
            if(index + intervalo > maior_long):
                k -= 1
            break
        k += 1
    for j in range(0, int(max_range_lat), int(end_range_lat)):
        #Viu? Tirei o 100000000 que eu havia multiplicado
        index = float(j)/100000000 + menor_lat
        if(obs_lat >= index and obs_lat < (index + intervalo)):
            if(index + intervalo > menor_lat):
                l -= 1
            break
        l += 1
    index = k*45 + l#matriz[i,j] -> vetor[i*45 + j], i = long, j = lat

    return int(index)

#@profile
def cria_vector(total_size, nome, t_abertura, menor_lat, menor_long, ano):
    f = open(nome, t_abertura)
    N, N_ano= 0, 0
    vector_quantidade = [0]*(total_size)

    # kanto region
    for line in f:
        parTerremoto = str.split(str(line))

        if(int(parTerremoto[2]) == ano):
            N_ano +=1
            obs_long = float(parTerremoto[0])
            obs_lat = float(parTerremoto[1])

            if(obs_long > menor_long and obs_long < maior_long):                    
                if(obs_lat > menor_lat and obs_lat < maior_lat):
                    if(float(parTerremoto[6]) <= depth):
                        if(float(parTerremoto[5]) >= mag):
                            index = calc_grupo_coord(obs_long, obs_lat, menor_lat, menor_long)

                            if(index < 0 or index > 2024):
                                print "Deu erro no index: ", index
                                exit(0)
                            vector_quantidade[index] += 1
        N += 1
    f.close()
    return vector_quantidade, N, sum(vector_quantidade)

#@profile
def calcular_expectations(modified_quant_por_grupo, total_size, N):

    expectations = [0.0] * (total_size)
    for l in xrange(total_size):
        expectations[l] = (float(modified_quant_por_grupo[l])/float(N))
    return expectations

#@profile
def poisson_press(prob,mi): #prob e o valor do bin

    if(mi >= 0):
        if(prob >= 0):
            if(prob < 1):
                l = math.exp(-mi)
                k = 1
                p = 1 * prob
                while(p > l):
                    k += 1
                    p = p * prob
                return (k)


#@profile
def dados_observados_R(ano):
    
    global quant_por_grupo
    quant_por_grupo, N, N_anoRegiao = cria_vector(total_size, arq_entrada, 'r', menor_lat, menor_long, ano)
    
    return quant_por_grupo, N, N_anoRegiao

#@profile
def log_likelihood(quant_por_grupoMODELO):

    log_likelihood =  [0]*(total_size)
    joint_log_likelihood = long(0)
    descarta_Modelo = False


    for i in range(total_size):
        if quant_por_grupoMODELO[i] == 0:
            quant_por_grupoMODELO[i] += 1
        if (quant_por_grupo[i] == 0 and quant_por_grupoMODELO[i] == 0):
          log_likelihood[i] += 1      
        elif (quant_por_grupo[i] != 0 and quant_por_grupoMODELO[i] == 0):
          log_likelihood[i] = Decimal('-Infinity')
          descarta_Modelo = True
        if(quant_por_grupo[i] > 100):
            cast = 99
        else:
            cast = quant_por_grupo[i]
        log_likelihood[i] = -quant_por_grupoMODELO[i] + (quant_por_grupo[i]*math.log10(quant_por_grupoMODELO[i])) - (math.log10(float(fatorial[cast])))

    #calcula o joint_log_likelihood
    joint_log_likelihood = sum(log_likelihood)

    return log_likelihood, joint_log_likelihood, descarta_Modelo



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
    global mi
    
    quant_por_grupoMODELO = [0] * len(individual)
    for i in range(len(individual)):
        quant_por_grupoMODELO[i] = poisson_press(individual[i], mi)
        if(quant_por_grupoMODELO[i] == None):
            print  individual[i], quant_por_grupo[i]
            exit(0)
    log_likelihood_ind, log_likelihood_total, descarta_modelo = log_likelihood(quant_por_grupoMODELO)

    return log_likelihood_total,

# Operator registering
toolbox.register("evaluate", evalOneMax)
if(int(sys.argv[2]) == 0):
    toolbox.register("mate", tools.cxOnePoint)
elif(int(sys.argv[2]) == 1):
    toolbox.register("mate", tools.cxTwoPoints)
elif(int(sys.argv[2]) == 2):
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
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
    toolbox.register("mutate", tools.mutPolynomialBounded,indpb=0.05, eta = 1, low = 0, up = 1)#float

if(int(sys.argv[4]) == 23):
    toolbox.register("select", tools.selTournament, tournsize=50)
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
    CXPB, MUTPB, NGEN, cumulative = 0.9, 0.1, 100, 0.8
    ano, ano_limite = 2000, 2010

    ano_teste = ano + slices    

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = "gen","time","min","avg","max","std"
    starttime = time.time()
    
    while(ano_teste <= ano_limite):
        global mi
        mi = calculo_lambda(ano)
        

        quant_por_grupo, N, N_anoRegiao = dados_observados_R(ano_teste)

        pop = toolbox.population(n=500)

        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        # Begin the evolution())
        for g in range(NGEN):
            print("-- Generation %i --" % g)
            # Select the next generation individuals
            offspring = toolbox.select(pop, 50)
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))
            # Apply crossover and mutation on the offspring
            m = 0
            cx, mut = 0,0
            while (m < 50):
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < CXPB:
                        toolbox.mate(child1, child2)
                        del child1.fitness.values
                        del child2.fitness.values
                        m += 2
                        cx +=1
            m = 0
            limite = 50 - cx
            while(m < limite):
                for mutant in offspring:
                    if random.random() < MUTPB:
                        i = 0
                        chance = 1
                        for bin in mutant:
                            if random.random() < chance:
                                mutant[i] = random.random()
                                chance *= cumulative
                                i += 1
                        del mutant.fitness.values
                        m += 1
                    if (m >= limite):
                        break
            # Evaluate the individuals with an invalid fitness

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            for i in range(len(invalid_ind)):
                for j in range(len(invalid_ind[i])):
                    if(invalid_ind[i][j] < 0):
                        invalid_ind[i][j] = -invalid_ind[i][j]
                    if(invalid_ind[i][j] > 1):
                        invalid_ind[i][j] = random.random()

            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            
            # The population is entirely replaced by the offspring, but the last pop best_ind

            best_ind = tools.selBest(pop, 1)[0]
            worst_ind = tools.selWorst(offspring, 1)[0]

            for i in range(len(offspring)):
                if (offspring[i] == worst_ind):
                    offspring[i] = best_ind
                    break

            CXPB, MUTPB = CXPB - (0.003), MUTPB + (0.003)
            pop[:] = offspring  
            record = stats.compile(pop)
            melhor = stats.compile(best_ind)
            logbook.record(gen=g,time=time.time()-starttime,**record, **melhor, **ano)

            # fim loop GERACAO
        CXPB, MUTPB = 0.9, 0.1
        ano += 1
        ano_teste = ano + slices

        MODELO = [0] * total_size
        best_ind = tools.selBest(pop, 1)[0]

        for i in range(len(best_ind)):
            # quant_por_grupo
            MODELO[i] = poisson_press(best_ind[i],mi) 
 
        while True:
            try:            
                f = open(sys.argv[1], "a")
                flock(f, LOCK_EX | LOCK_NB)
                f.write(str(ano_teste))
                f.write('\n')
                f.write(str(MODELO))
                f.write('\n')
                flock(f, LOCK_UN)
                f.write('\n')
                f.close()
                f = open('logBook/'"AA"+ str(ano_teste) + str(' ') + sys.argv[2]+sys.argv[3]+sys.argv[4], "a")
                flock(f, LOCK_EX | LOCK_NB)
                f.write(str(logbook))
                f.write('\n')
                flock(f, LOCK_UN)
                f.close()
            except IOError:
                time.sleep(5)
                continue
            break

        


if __name__ == "__main__":
    main()