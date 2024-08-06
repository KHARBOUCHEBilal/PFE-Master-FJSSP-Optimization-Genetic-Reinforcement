#!/usr/bin/env python

import sys

# Objectif: Séparer le vecteur ms (machine sequence) en sous-séquences correspondant à chaque travail.
# Entrées:
# pb_instance: Instance du problème, contenant les détails des travaux.
# ms: Séquence des machines.
# Sortie: Liste des sous-séquences de machines pour chaque travail.
def split_ms(pb_instance, ms):
    """
    Sépare le vecteur ms (séquence des machines) en sous-séquences correspondant à chaque travail.
    :param pb_instance: Dictionnaire contenant les détails des travaux.
    :param ms: Liste des machines.
    :return: Liste des sous-séquences de machines pour chaque travail.
    """
    jobs = []
    current = 0
    for index, job in enumerate(pb_instance['jobs']):
        jobs.append(ms[current:current+len(job)])
        current += len(job)

    return jobs

# Objectif: Trouver le temps de traitement d'une opération sur une machine donnée.
# Entrées:
# op_by_machine: Liste des opérations par machine.
# machine_nb: Numéro de la machine.
# Sortie: Temps de traitement de l'opération sur la machine spécifiée.
def get_processing_time(op_by_machine, machine_nb):
    """
    Trouve le temps de traitement d'une opération sur une machine donnée.
    :param op_by_machine: Liste des opérations par machine.
    :param machine_nb: Numéro de la machine.
    :return: Temps de traitement de l'opération sur la machine spécifiée.
    """
    for op in op_by_machine:
        if op['machine'] == machine_nb:
            return op['processingTime']
    print("[ERROR] Machine {} doesn't to be able to process this task.".format(machine_nb))
    sys.exit(-1)

# Objectif: Vérifier si un intervalle de temps est libre sur une machine.
# Entrées:
# tab: Tableau indiquant les plages horaires utilisées.
# start: Début de l'intervalle.
# duration: Durée de l'intervalle.
# Sortie: True si l'intervalle est libre, sinon False.
def is_free(tab, start, duration):
    """
    Vérifie si un intervalle de temps est libre sur une machine.
    :param tab: Tableau indiquant les plages horaires utilisées.
    :param start: Début de l'intervalle.
    :param duration: Durée de l'intervalle.
    :return: True si l'intervalle est libre, sinon False.
    """
    for k in range(start, start+duration):
        if not tab[k]:
            return False
    return True

# Objectif: Trouver le premier intervalle de temps disponible pour une opération sur une machine.
# Entrées:
# start_ctr: Début de la contrainte.
# duration: Durée de l'opération.
# machine_jobs: Liste des opérations sur la machine.
# Sortie: Premier temps disponible pour l'opération.
def find_first_available_place(start_ctr, duration, machine_jobs):
    """
    Trouve le premier intervalle de temps disponible pour une opération sur une machine.
    :param start_ctr: Début de la contrainte.
    :param duration: Durée de l'opération.
    :param machine_jobs: Liste des opérations sur la machine.
    :return: Premier temps disponible pour l'opération.
    """
    max_duration_list = []
    max_duration = start_ctr + duration

    # max_duration is either the start_ctr + duration or the max(possible starts) + duration
    if machine_jobs:
        for job in machine_jobs:
            max_duration_list.append(job[3] + job[1])  # start + process time

        max_duration = max(max(max_duration_list), start_ctr) + duration

    machine_used = [True] * max_duration

    # Mettre à jour le tableau avec les plages horaires utilisées
    for job in machine_jobs:
        start = job[3]
        long = job[1]
        for k in range(start, start + long):
            machine_used[k] = False

    # Trouver le premier intervalle de temps disponible qui respecte la contrainte
    for k in range(start_ctr, len(machine_used)):
        if is_free(machine_used, k, duration):
            return k

# Objectif: Décoder la séquence des opérations (os) et des machines (ms) en un plan de production détaillé.
# Entrées:
# pb_instance: Instance du problème.
# os: Séquence des opérations.
# ms: Séquence des machines.
# Sortie: Liste des opérations planifiées sur chaque machine.
def decode(pb_instance, os, ms):
    """
    Décode la séquence des opérations (os) et des machines (ms) en un plan de production détaillé.
    :param pb_instance: Instance du problème.
    :param os: Séquence des opérations.
    :param ms: Séquence des machines.
    :return: Liste des opérations planifiées sur chaque machine.
    """
    o = pb_instance['jobs']
    machine_operations = [[] for i in range(pb_instance['machinesNb'])]

    ms_s = split_ms(pb_instance, ms)  # machine pour chaque opération

    indexes = [0] * len(ms_s)
    start_task_cstr = [0] * len(ms_s)

    # Itération sur OS pour obtenir l'ordre d'exécution des tâches et vérifier dans
    # MS pour obtenir la machine
    for job in os:
        index_machine = ms_s[job][indexes[job]]
        machine = o[job][indexes[job]][index_machine]['machine']
        prcTime = o[job][indexes[job]][index_machine]['processingTime']
        start_cstr = start_task_cstr[job]

        # Obtenir le premier intervalle de temps disponible pour l'opération
        start = find_first_available_place(start_cstr, prcTime, machine_operations[machine - 1])
        name_task = "OP_{}-{}".format(job + 1, indexes[job] + 1)

        machine_operations[machine - 1].append((name_task, prcTime, start_cstr, start))

        # Mise à jour des index (un pour la tâche actuelle pour chaque travail, un pour la contrainte de début
        # pour chaque travail)
        indexes[job] += 1
        start_task_cstr[job] = (start + prcTime)

    return machine_operations


# Objectif: Convertir les opérations planifiées en un format utilisable pour générer un diagramme de Gantt.
# Entrées:
# machine_operations: Liste des opérations planifiées sur chaque machine.
# Sortie: Dictionnaire formaté pour un diagramme de Gantt.
def translate_decoded_to_gantt(machine_operations):
    """
    Convertit les opérations planifiées en un format utilisable pour générer un diagramme de Gantt.
    :param machine_operations: Liste des opérations planifiées sur chaque machine.
    :return: Dictionnaire formaté pour un diagramme de Gantt.
    """
    data = {}
    print("____ translate decode to gantt ____")
    print("machine operations : ", machine_operations)
    for idx, machine in enumerate(machine_operations):
        print("idx ", idx, "machine ", machine)
        machine_name = "Machine-{}".format(idx + 1)
        print("machine name ", machine_name)
        operations = []
        for operation in machine:
            print("operation in machine ", operation)
            operations.append([operation[3], operation[3] + operation[1], operation[0]])
        operations
        data[machine_name] = operations
        print("data[machine name] : ", data[machine_name])

    return data