#!/usr/bin/env python

# Ce module crée une population de chromosomes OS et MS aléatoires.

import random
from src import config

def generateOS(parameters):
    """
    Génère un chromosome OS (Ordre des Séquences) aléatoire pour les jobs.
    :param parameters: Dictionnaire contenant les informations des jobs.
    :return: Liste représentant le chromosome OS.
    """
    jobs = parameters['jobs']

    OS = []
    i = 0
    for job in jobs:
        for op in job:
            OS.append(i)
        i = i + 1
    # Mélange aléatoire des éléments du chromosome OS
    random.shuffle(OS)

    return OS

def generateMS(parameters):
    """
    Génère un chromosome MS (Sélection des Machines) aléatoire pour les jobs.
    :param parameters: Dictionnaire contenant les informations des jobs.
    :return: Liste représentant le chromosome MS.
    """
    jobs = parameters['jobs']
    MS = []
    for job in jobs:
        for op in job:
            # Sélection aléatoire d'une machine pour chaque opération
            randomMachine = random.randint(0, len(op) - 1)
            MS.append(randomMachine)
        
    return MS

def initializePopulation(parameters):
    """
    Initialise la population avec des chromosomes OS et MS aléatoires.
    :param parameters: Dictionnaire contenant les informations des jobs.
    :return: Liste de tuples représentant la population initiale de chromosomes (OS, MS).
    """
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))

    return gen1
