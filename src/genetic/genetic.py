#!/usr/bin/env python

# Ce module contient l'implémentation détaillée de chaque opérateur génétique.
# Le code suit strictement la section 4.3 de l'article fourni.

import random
import itertools
from src import config
from src.genetic import decoding

# Objectif: Calculer le temps total nécessaire pour exécuter un ensemble d'opérations et de machines.
# Entrées:
    ## os_ms: Un tuple contenant la séquence des opérations (os) et la séquence des machines (ms).
    ## pb_instance: L'instance du problème.
# Sortie: Le temps maximal requis par n'importe quelle machine.
def timeTaken(os_ms, pb_instance):
    """
    Calcule le temps total nécessaire pour exécuter un ensemble d'opérations et de machines.
    :param os_ms: Tuple contenant la séquence des opérations (os) et la séquence des machines (ms).
    :param pb_instance: Dictionnaire contenant les détails des travaux.
    :return: Le temps maximal requis par n'importe quelle machine.
    """
    (os, ms) = os_ms
    decoded = decoding.decode(pb_instance, os, ms)

    # Obtenir le maximum pour chaque machine
    max_per_machine = []
    for machine in decoded:
        max_d = 0
        for job in machine:
            end = job[3] + job[1]
            if end > max_d:
                max_d = end
        max_per_machine.append(max_d)

    return max(max_per_machine)


# 4.3.1 Sélection
#######################
# Objectif: Sélectionner les meilleurs individus de la population.
# Détails: Trie la population par le temps pris et garde un pourcentage (pr) des meilleurs individus.
def elitistSelection(population, parameters):
    """
    Sélectionne les meilleurs individus de la population.
    :param population: Liste des individus de la population.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Liste des meilleurs individus sélectionnés.
    """
    keptPopSize = int(config.pr * len(population))
    sortedPop = sorted(population, key=lambda cpl: timeTaken(cpl, parameters))
    return sortedPop[:keptPopSize]

def tournamentSelection(population, parameters):
    """
    Sélectionne des individus par tournoi.
    :param population: Liste des individus de la population.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Individu sélectionné.
    """
    b = 2

    selectedIndividuals = []
    for i in range(b):
        randomIndividual = random.randint(0, len(population) - 1)
        selectedIndividuals.append(population[randomIndividual])

    return min(selectedIndividuals, key=lambda cpl: timeTaken(cpl, parameters))

def selection(population, parameters):
    """
    Sélectionne les individus pour la nouvelle population.
    :param population: Liste des individus de la population.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Nouvelle population sélectionnée.
    """
    newPop = elitistSelection(population, parameters)
    while len(newPop) < len(population):
        newPop.append(tournamentSelection(population, parameters))

    return newPop


# 4.3.2 Opérateurs de croisement
###########################

def precedenceOperationCrossover(p1, p2, parameters):
    """
    Opérateur de croisement par priorité d'opérations.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Tuple des enfants (o1, o2).
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(1, jobNumber+1)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def jobBasedCrossover(p1, p2, parameters):
    """
    Opérateur de croisement basé sur les travaux.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Tuple des enfants (o1, o2).
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(0, jobNumber)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def twoPointCrossover(p1, p2):
    """
    Opérateur de croisement à deux points.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :return: Tuple des enfants (offspring1, offspring2).
    """
    pos1 = random.randint(0, len(p1) - 1)
    pos2 = random.randint(0, len(p1) - 1)

    if pos1 > pos2:
        pos2, pos1 = pos1, pos2

    offspring1 = p1
    if pos1 != pos2:
        offspring1 = p1[:pos1] + p2[pos1:pos2] + p1[pos2:]

    offspring2 = p2
    if pos1 != pos2:
        offspring2 = p2[:pos1] + p1[pos1:pos2] + p2[pos2:]

    return (offspring1, offspring2)

def crossoverOS(p1, p2, parameters):
    """
    Applique un croisement sur les séquences d'opérations (OS).
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Tuple des enfants (oOS1, oOS2).
    """
    if random.choice([True, False]):
        return precedenceOperationCrossover(p1, p2, parameters)
    else:
        return jobBasedCrossover(p1, p2, parameters)

def crossoverMS(p1, p2):
    """
    Applique un croisement à deux points sur les séquences de machines (MS).
    :param p1: Parent 1.
    :param p2: Parent 2.
    :return: Tuple des enfants (oMS1, oMS2).
    """
    return twoPointCrossover(p1, p2)

def crossover(population, parameters, pc):
    """
    Applique le croisement sur la population entière.
    :param population: Liste des individus de la population.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Nouvelle population après croisement.
    """
    newPop = []
    i = 0
    while i < len(population):
        (OS1, MS1) = population[i]
        (OS2, MS2) = population[i+1]

        if random.random() < pc:
            (oOS1, oOS2) = crossoverOS(OS1, OS2, parameters)
            (oMS1, oMS2) = crossoverMS(MS1, MS2)
            newPop.append((oOS1, oMS1))
            newPop.append((oOS2, oMS2))
        else:
            newPop.append((OS1, MS1))
            newPop.append((OS2, MS2))

        i = i + 2

    return newPop


# 4.3.3 Opérateurs de mutation
##########################

def swappingMutation(p):
    """
    Opérateur de mutation par échange.
    :param p: Individu à muter.
    :return: Individu muté.
    """
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring = p[:pos1] + [p[pos2]] + \
          p[pos1+1:pos2] + [p[pos1]] + \
          p[pos2+1:]

    return offspring

def neighborhoodMutation(p):
    """
    Opérateur de mutation par voisinage.
    :param p: Individu à muter.
    :return: Individu muté.
    """
    pos3 = pos2 = pos1 = random.randint(0, len(p) - 1)

    while p[pos2] == p[pos1]:
        pos2 = random.randint(0, len(p) - 1)

    while p[pos3] == p[pos2] or p[pos3] == p[pos1]:
        pos3 = random.randint(0, len(p) - 1)

    sortedPositions = sorted([pos1, pos2, pos3])
    pos1 = sortedPositions[0]
    pos2 = sortedPositions[1]
    pos3 = sortedPositions[2]

    e1 = p[sortedPositions[0]]
    e2 = p[sortedPositions[1]]
    e3 = p[sortedPositions[2]]

    permutations = list(itertools.permutations([e1, e2, e3]))
    permutation  = random.choice(permutations)

    offspring = p[:pos1] + [permutation[0]] + \
          p[pos1+1:pos2] + [permutation[1]] + \
          p[pos2+1:pos3] + [permutation[2]] + \
          p[pos3+1:]

    return offspring

def halfMutation(p, parameters):
    """
    Opérateur de mutation par moitié.
    :param p: Individu à muter.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Individu muté.
    """
    o = p
    jobs = parameters['jobs']

    size = len(p)
    r = int(size/2)

    positions = random.sample(range(size), r)

    i = 0
    for job in jobs:
        for op in job:
            if i in positions:
                o[i] = random.randint(0, len(op)-1)
            i = i+1

    return o

def mutationOS(p):
    """
    Applique une mutation sur les séquences d'opérations (OS).
    :param p: Individu à muter.
    :return: Individu muté.
    """
    if random.choice([True, False]):
        return swappingMutation(p)
    else:
        return neighborhoodMutation(p)

def mutationMS(p, parameters):
    """
    Applique une mutation par moitié sur les séquences de machines (MS).
    :param p: Individu à muter.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Individu muté.
    """
    return halfMutation(p, parameters)

def mutation(population, parameters, pm):
    """
    Applique la mutation sur la population entière.
    :param population: Liste des individus de la population.
    :param parameters: Dictionnaire contenant les détails des travaux.
    :return: Nouvelle population après mutation.
    """
    newPop = []

    for (OS, MS) in population:
        if random.random() < pm:
            oOS = mutationOS(OS)
            oMS = mutationMS(MS, parameters)
            newPop.append((oOS, oMS))
        else:
            newPop.append((OS, MS))

    return newPop
