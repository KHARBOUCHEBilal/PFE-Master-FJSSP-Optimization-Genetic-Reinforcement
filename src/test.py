#!/usr/bin/env python

from src.genetic import genetic, encoding

# Ce script exécute chaque partie non triviale du code défini dans ce projet pour tester facilement leur comportement

print("=== Génération OS & MS ===")
# Définition des opérations pour chaque job
op11 = [{'machine': 0, 'processingTime': 1}, {'machine': 1, 'processingTime': 2}]
op12 = [{'machine': 1, 'processingTime': 1}, {'machine': 2, 'processingTime': 2}]
job1 = [op11, op12]
op21 = [{'machine': 2, 'processingTime': 1}, {'machine': 3, 'processingTime': 2}]
op22 = [{'machine': 3, 'processingTime': 1}, {'machine': 4, 'processingTime': 2}]
job2 = [op21, op22]
op31 = [{'machine': 4, 'processingTime': 1}, {'machine': 5, 'processingTime': 2}]
op32 = [{'machine': 5, 'processingTime': 1}, {'machine': 0, 'processingTime': 2}]
job3 = [op31, op32]
jobs = [job1, job2, job3]

# Test de la génération de OS (Ordre des Séquences) et MS (Sélection des Machines)
print("OS: " + str(encoding.generateOS({'machinesNb': 6, 'jobs': jobs})))
print("MS: " + str(encoding.generateMS({'machinesNb': 6, 'jobs': jobs})))

print("=== SÉLECTION ===")
# Définition d'une population pour tester la sélection
pop = [([1, 3, 1, 2, 2, 3], [2, 1, 3, 1, 2, 2]),
       ([1, 1, 2, 2, 3, 3], [1, 2, 3, 1, 2, 3]),
       ([3, 2, 1, 1, 2, 3], [1, 1, 1, 1, 1, 1])]
# Test de la sélection élitiste et par tournoi
print("elitist: " + str(genetic.elitistSelection(pop, {'jobs': jobs, 'machinesNb': 6})))
print("tournament: " + str(genetic.tournamentSelection(pop, {'jobs': jobs, 'machinesNb': 6})))

print("=== MUTATION ===")
# Définition d'un individu pour tester la mutation
p = [0, 1, 2, 3, 4, 5]

# Test des différents types de mutation
print("swapping: " + str(genetic.swappingMutation(p)))
print("neighborghood: " + str(genetic.neighborhoodMutation(p)))
print("half: " + str(genetic.halfMutation(p, {'machinesNb': 6, 'jobs': jobs})))

print("=== CROISEMENT ===")
# Définition de deux parents pour tester le croisement
p1 = [1, 3, 1, 2, 2, 3]
p2 = [3, 2, 1, 2, 3, 1]

# Test des différents types de croisement
print("POX: " + str(genetic.precedenceOperationCrossover(p1, p2, {'jobs': jobs})))
print("JBX: " + str(genetic.jobBasedCrossover(p1, p2, {'jobs': jobs})))
print("two point: " + str(genetic.twoPointCrossover(p1, p2)))
