import os
import time
import csv
import numpy as np
import random
from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

def initialize_SLGA_parameters():
    # Initialisation des paramètres du SLGA
    Pc_range = (0.4, 0.9)
    Pm_range = (0.01, 0.21)
    epsilon = 0.1
    alpha = 0.1
    gamma = 0.9
    return Pc_range, Pm_range, epsilon, alpha, gamma

def initialize_Q_table(population_size):
    return np.zeros((population_size, 2))  # Deux actions possibles: ajuster Pc ou Pm

def update_Q_sarsa(Q, state, action, reward, next_state, next_action, alpha, gamma):
    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + gamma * Q[next_state][next_action])
    return Q

def update_Q_qlearning(Q, state, action, reward, next_state, alpha, gamma):
    max_Q_next = max(Q[next_state])
    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + gamma * max_Q_next)
    return Q

def run_genetic_algorithm(data_path, output_prefix):

    # pour l'arret si pas d'imporvement 
    max_no_improvement_generations = 50
    no_improvement_count = 0
    previous_best_time = float('inf')  # Un grand nombre au début
    print("initalia the max no imporvement generations ", max_no_improvement_generations)
    print("_" * 30)

    # Initialisation des paramètres pour chaque test
    Pc_range, Pm_range, epsilon, alpha, gamma = initialize_SLGA_parameters()
    print("Pc range : ", Pc_range)
    print("Pm_range : ", Pm_range)
    print("epsilon : ", epsilon)
    print("alpha : ", alpha)
    print("gamma : ", gamma)
    print("_" * 30)

    # Paramètres contient la data 
    parameters = parser.parse(data_path)
   
    # Initialiser la population
    population = encoding.initializePopulation(parameters)
    
    # Initialiser la table Q
    Q = initialize_Q_table(len(population))
    
    # Dessiner et sauvegarder le diagramme de Gantt initial
    
    initial_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
    initial_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, initial_best_individual[0], initial_best_individual[1]))
    print("initial - gannt data : ", initial_gantt_data)
    print("inital best 0 : ", initial_best_individual[0])
    print("inital best 1 : ", initial_best_individual[1])
    print("paramters : ", parameters)
    gantt.draw_chart(initial_gantt_data, f'{output_prefix}_initial_gantt.svg')
    print("< gantt >")
    print(f"Diagramme de Gantt initial sauvegardé sous '{output_prefix}_initial_gantt.svg'.")
    t0 = time.time()  # Temps de début

    gen = 1  # Initialisation de la génération
    use_sarsa = True  # Commencer par SARSA

    # Initialiser la liste pour enregistrer les étapes
    steps = []
    print("boucle ")
    # Évaluer la population
    while not termination.shouldTerminate(population, gen) and no_improvement_count < max_no_improvement_generations:
        print(f"Génération {gen}")
        best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        best_time = genetic.timeTaken(best_individual, parameters)
        print(f"Meilleur temps dans la génération {gen}: {best_time}")


        # Mise à jour de l'amélioration
        if best_time == previous_best_time:
            no_improvement_count += 1
        else:
            no_improvement_count = 0

        previous_best_time = best_time

        
        # Enregistrer l'étape actuelle
        steps.append({'generation': gen, 'best_time': best_time})

        # Sélection de l'action basée sur epsilon-greedy
        state = gen % len(population)
        Pc = random.uniform(*Pc_range)  # Initialiser Pc
        Pm = random.uniform(*Pm_range)  # Initialiser Pm
        if random.random() < epsilon:
            action = random.choice([0, 1])  # Exploration
        else:
            action = np.argmax(Q[state])  # Exploitation

        # Ajustement de Pc et Pm selon l'action choisie
        if action == 0:
            Pc = random.uniform(*Pc_range)
        else:
            Pm = random.uniform(*Pm_range)

        # Opérateurs génétiques avec Pc et Pm ajustés
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters, Pc)  # Pc utilisé ici
        population = genetic.mutation(population, parameters, Pm)  # Pm utilisé ici

        # Choix de la prochaine action pour SARSA
        if random.random() < epsilon:
            next_action = random.choice([0, 1])  # Exploration
        else:
            next_action = np.argmax(Q[(gen + 1) % len(population)])  # Exploitation

        # Mise à jour des valeurs Q selon SARSA ou Q-learning
        new_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        new_best_time = genetic.timeTaken(new_best_individual, parameters)
        reward = (best_time - new_best_time) / best_time

        if use_sarsa:
            Q = update_Q_sarsa(Q, state, action, reward, (gen + 1) % len(population), next_action, alpha, gamma)
        else:
            Q = update_Q_qlearning(Q, state, action, reward, (gen + 1) % len(population), alpha, gamma)

        # Passer de SARSA à Q-learning après un certain nombre d'itérations
        if gen > (len(population) * 10):  # Critère de transition
            use_sarsa = False

        gen += 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()  # Temps de fin
    total_time = t1 - t0  # Temps total
    print("Terminé en {0:.2f}s".format(total_time))

    # Dessiner et sauvegarder le diagramme de Gantt final
    final_gantt_data = decoding.translate_decoded_to_gantt(decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1]))
    gantt.draw_chart(final_gantt_data, f'{output_prefix}_final_gantt.svg')
    print(f"Diagramme de Gantt final sauvegardé sous '{output_prefix}_final_gantt.svg'.")

    # Enregistrer les étapes et le temps total dans un fichier CSV
    with open(f'{output_prefix}_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['generation', 'best_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for step in steps:
            writer.writerow(step)
        writer.writerow({'generation': 'Total Time', 'best_time': total_time})

    print(f"Résultats sauvegardés sous '{output_prefix}_results.csv'.")

def main():
    data_dir = 'test_data/Brandimarte_Data/Text'
    output_dir = 'comparison_results'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.fjs'):
            data_path = os.path.join(data_dir, file_name)
            output_prefix = os.path.join(output_dir, os.path.splitext(file_name)[0])
            print(f"Running genetic algorithm on {file_name}...")
            run_genetic_algorithm(data_path, output_prefix)
            print(f"Finished processing {file_name}.\n")
    # data_dir = 'test_data/Brandimarte_Data/Text'
    # output_dir = 'comparison_results'
    
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    
    # specific_instance = 'Mk03.fjs'
    # data_path = os.path.join(data_dir, specific_instance)
    # output_prefix = os.path.join(output_dir, os.path.splitext(specific_instance)[0])
    # try:
    #     print(f"Running genetic algorithm on {specific_instance}...")
    #     run_genetic_algorithm(data_path, output_prefix)
    #     print(f"Finished processing {specific_instance}.\n")
    # except Exception as e:
    #     print(f"An error occurred while processing {specific_instance}: {e}")
    #     import traceback
    #     traceback.print_exc()

if __name__ == "__main__":
    main()
