#!/usr/bin/env python

# Ce module analyse les fichiers .fjs tels qu'on les trouve dans le dataset "Monaldo" FJSP.
# Plus d'explications sur ce format de fichier peuvent être trouvées dans le dataset.

def parse(path):
    """
    Analyse un fichier .fjs et extrait les informations sur les travaux et les machines.
    :param path: Chemin vers le fichier .fjs à analyser.
    :return: Dictionnaire contenant le nombre de machines et les détails des travaux.
    """
    file = open(path, 'r')  # Ouvre le fichier en lecture

    firstLine = file.readline()  # Lit la première ligne du fichier
    firstLineValues = list(map(int, firstLine.split()[0:2]))  # Extrait les deux premiers entiers de la première ligne

    jobsNb = firstLineValues[0]  # Nombre de travaux
    machinesNb = firstLineValues[1]  # Nombre de machines

    jobs = []  # Liste pour stocker les travaux

    for i in range(jobsNb):
        currentLine = file.readline()  # Lit la ligne actuelle
        currentLineValues = list(map(int, currentLine.split()))  # Convertit les valeurs de la ligne en entiers
        operations = []  # Liste pour stocker les opérations du travail (job) actuel
        j = 1
        while j < len(currentLineValues):
            k = currentLineValues[j]  # Nombre d'opérations pour la machine actuelle
            j = j + 1
            operation = []  # Liste pour stocker les détails de chaque opération
            for ik in range(k):
                # print("ik ", ik)
                # print(" j ", j)
                machine = currentLineValues[j]  # Numéro de la machine
                # print("machine ", machine)
                j = j + 1
                processingTime = currentLineValues[j]  # Temps de traitement
                # print("processing Time ", processingTime)
                j = j + 1

                operation.append({'machine': machine, 'processingTime': processingTime})  # Ajoute l'opération à la liste

            operations.append(operation)  # Ajoute les opérations du travail actuel à la liste des travaux

        jobs.append(operations)  # Ajoute le travail à la liste des travaux

    file.close()  # Ferme le fichier

    return {'machinesNb': machinesNb, 'jobs': jobs}  # Retourne un dictionnaire contenant le nombre de machines et les travaux

# Test du parser
data = parse('./test_data/Brandimarte_Data/Text/Mk01.fjs')
print("Données parsées:", data)
