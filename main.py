#!/usr/bin/env python

# This script contains a high-level overview of the proposed hybrid algorithm
# and displays the Gantt charts before and after applying the genetic algorithm.

import sys
import time

from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

# Beginning
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " filename")
else:
    # Parameters Setting
    parameters = parser.parse(sys.argv[1])

    # Initialize the Population
    population = encoding.initializePopulation(parameters)
    
    # Draw and save initial Gantt chart
    initial_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
    initial_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, initial_best_individual[0], initial_best_individual[1]))
    gantt.draw_chart(initial_gantt_data, 'initial_gantt.svg')
    print("Initial Gantt chart saved as 'initial_gantt.svg'.")
    
    t0 = time.time()

    gen = 1

    # Evaluate the population
    while not termination.shouldTerminate(population, gen):
        print(f"Generation {gen}")
        best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        best_time = genetic.timeTaken(best_individual, parameters)
        print(f"Best time in generation {gen}: {best_time}")

        # Genetic Operators
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters)
        population = genetic.mutation(population, parameters)

        gen += 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()
    total_time = t1 - t0
    print("Finished in {0:.2f}s".format(total_time))

    # Draw and save final Gantt chart
    final_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))
    gantt.draw_chart(final_gantt_data, 'final_gantt.svg')
    print("Final Gantt chart saved as 'final_gantt.svg'.")
