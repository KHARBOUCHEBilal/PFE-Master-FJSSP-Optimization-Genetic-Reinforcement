#!/usr/bin/env python

# Ce script contient une vue d'ensemble de l'algorithme hybride proposé
# et affiche les diagrammes de Gantt avant et après l'application de l'algorithme génétique.

import sys
import time

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

# Début du script
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Paramètres contient la data 
    parameters = parser.parse(sys.argv[1])
    # Initialiser la population
    population = encoding.initializePopulation(parameters)
    # Dessiner et sauvegarder le diagramme de Gantt initial
    initial_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
    print("initial best individual ", initial_best_individual)
    print("population ", population)
    initial_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, initial_best_individual[0], initial_best_individual[1]))
    gantt.draw_chart(initial_gantt_data, 'initial_gantt_i.svg')
    print("Diagramme de Gantt initial sauvegardé sous 'initial_gantt.svg'.")
    t0 = time.time()  # Temps de début

    gen = 1  # Initialisation de la génération
    # Évaluer la population
    while not termination.shouldTerminate(population, gen):
        print(f"Génération {gen}")
        best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        best_time = genetic.timeTaken(best_individual, parameters)
        print(f"Meilleur temps dans la génération {gen}: {best_time}")

        # Opérateurs génétiques
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        gen += 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()  # Temps de fin
    total_time = t1 - t0  # Temps total
    print("Terminé en {0:.2f}s".format(total_time))

    # Dessiner et sauvegarder le diagramme de Gantt final
    final_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))
    gantt.draw_chart(final_gantt_data, 'final_gantt_i.svg')
    print("Diagramme de Gantt final sauvegardé sous 'final_gantt.svg'.")
