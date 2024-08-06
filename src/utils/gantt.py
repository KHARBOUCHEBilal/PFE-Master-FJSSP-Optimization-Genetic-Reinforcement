#!/usr/bin/env python

# Ce module aide à créer des diagrammes de Gantt à partir d'un dictionnaire.
# Le format de sortie est un graphique Matplotlib.

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import colors as mcolors

# Fonction pour générer une liste de couleurs aléatoires
def generate_colors(n):
    """
    Génère une liste de n couleurs uniques.
    
    :param n: Nombre de couleurs à générer
    :return: Liste de couleurs
    """
    colors = list(mcolors.CSS4_COLORS.values())
    if n <= len(colors):
        return colors[:n]
    else:
        random_colors = []
        for i in range(n):
            random_colors.append((random.random(), random.random(), random.random()))
        return random_colors

# Initialiser le dictionnaire des couleurs des travaux avec une fonction de génération de couleurs
job_colors = {}

def calculate_makespan(data):
    """
    Calcule le makespan total à partir des données de planification.
    
    :param data: Dictionnaire contenant les données à tracer
    :return: Makespan total
    """
    max_end_time = 0
    for machine, operations in data.items():
        for op in operations:
            if op[1] > max_end_time:
                max_end_time = op[1]
    return max_end_time

def draw_chart(data, filename='gantt.svg'):
    """
    Dessine un diagramme de Gantt basé sur les données fournies et sauvegarde le diagramme sous forme de fichier SVG.
    
    :param data: Dictionnaire contenant les données à tracer
    :param filename: Nom du fichier de sortie pour le diagramme de Gantt
    """
    nb_row = len(data.keys())  # Nombre de machines
    pos = np.arange(0.5, nb_row * 0.5 + 0.5, 0.5)  # Positions pour les barres
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)
    index = 0
    max_len = []

    # Si nous n'avons pas assez de couleurs prédéfinies, générons plus de couleurs
    all_jobs = [int(op[2].split('_')[1].split('-')[0]) for machine, ops in data.items() for op in ops]
    unique_jobs = set(all_jobs)
    if len(unique_jobs) > len(job_colors):
        additional_colors = generate_colors(len(unique_jobs) - len(job_colors))
        for i, job in enumerate(unique_jobs):
            if job not in job_colors:
                job_colors[job] = additional_colors[i]

    for machine, operations in sorted(data.items()):
        for op in operations:
            max_len.append(op[1])  # Ajouter la longueur de l'opération pour définir les limites de l'axe x
            job_index = int(op[2].split('_')[1].split('-')[0])
            c = job_colors[job_index]
            rect = ax.barh((index * 0.5) + 0.5, op[1] - op[0], left=op[0], height=0.3, align='center',
                           edgecolor=c, color=c, alpha=0.8)

            # Ajouter l'étiquette
            width = int(rect[0].get_width())
            Str = "{}".format(op[2])
            xloc = op[0] + 0.50 * width
            clr = 'black'
            align = 'center'

            yloc = rect[0].get_y() + rect[0].get_height() / 2.0
            ax.text(xloc, yloc, Str, horizontalalignment=align,
                            verticalalignment='center', color=clr, weight='bold',
                            clip_on=True)
        index += 1

    ax.set_ylim(ymin=-0.1, ymax=nb_row * 0.5 + 0.5)
    ax.grid(color='gray', linestyle=':')
    ax.set_xlim(0, max(10, max(max_len)))

    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=14)

    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    ax.invert_yaxis()

    # Calculer le makespan total
    makespan = calculate_makespan(data)
    
    # Ajouter le makespan total au titre du graphique
    plt.title(f"Flexible Job Shop Solution - Makespan Total: {makespan}")

    plt.savefig(filename)
    plt.close(fig)  # Fermer la figure pour éviter de l'afficher
