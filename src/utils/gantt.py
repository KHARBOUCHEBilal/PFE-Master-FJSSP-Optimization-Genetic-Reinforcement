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
    Génère n couleurs distinctes en s'assurant qu'elles ne se répètent pas.
    :param n: Nombre de couleurs à générer.
    :return: Liste de couleurs RGB.
    """
    print("generation color n : ", n)
    base_colors = list(mcolors.CSS4_COLORS.values())  # Utilise les couleurs CSS4 pour plus de diversité
    random.shuffle(base_colors)  # Mélange les couleurs de base pour les diversifier
    colors = []
    print("Start boucle ")

    # Ajouter les couleurs de base jusqu'à ce qu'on atteigne le nombre requis ou qu'on les ait toutes utilisées
    for color in base_colors:
        if len(colors) >= n:
            break
        rgb_color = mcolors.to_rgb(color)
        if rgb_color not in colors:
            colors.append(rgb_color)

    # Si le nombre de jobs dépasse le nombre de couleurs disponibles, générer des couleurs supplémentaires
    while len(colors) < n:
        colors.append(mcolors.hsv_to_rgb([random.random(), 0.5 + 0.5 * random.random(), 1.0]))
    
    return colors

    """
    Génère n couleurs distinctes en s'assurant qu'elles ne se répètent pas.
    :param n: Nombre de couleurs à générer.
    :return: Liste de couleurs RGB.
    """
    print("generation color n : ", n)
    base_colors = list(mcolors.CSS4_COLORS.values())  # Utilise les couleurs CSS4 pour plus de diversité
    random.shuffle(base_colors)  # Mélange les couleurs de base pour les diversifier
    colors = []
    print("Start boucle ")
    while len(colors) < n:
        # print("line 25 ")
        # print("len of color ", len(colors), " ", n)
        color = random.choice(base_colors)  # Choisit une couleur de base aléatoire
        # print("color ", color)
        rgb_color = mcolors.to_rgb(color)  # Convertit en RGB
        
        if rgb_color not in colors:
            colors.append(rgb_color)  # Ajoute la couleur à la liste si elle est unique
        
        if len(colors) >= len(base_colors):  # Si on a utilisé toutes les couleurs de base, on arrête
            break
    print("out of boucle")
    # Si le nombre de jobs dépasse le nombre de couleurs disponibles, générer des couleurs supplémentaires
    while len(colors) < n:
        colors.append(mcolors.hsv_to_rgb([random.random(), 0.5 + 0.5 * random.random(), 1.0]))
    
    return colors

# Fonction pour dessiner le digramme de gantt 
def draw_chart(data, filename='gantt.svg'):
    """
    Dessine un diagramme de Gantt et le sauvegarde sous forme de fichier SVG.
    :param data: Dictionnaire contenant les opérations planifiées sur chaque machine.
    :param filename: Nom du fichier SVG de sortie.
    """
    nb_row = len(data.keys())  # Nombre de machines (lignes dans le diagramme)
    nb_jobs = sum(len(machine) for machine in data.values())  # Nombre total de jobs
    

    # Dictionnaire pour stocker les couleurs attribuées à chaque job
    job_colors = {}

    # Génère des couleurs supplémentaires en cas de grand nombre de jobs
    additional_colors = generate_colors(nb_jobs)
    # Positions des barres sur l'axe des y avec plus d'espace pour éviter les chevauchements
    pos = np.arange(0.5, nb_row * 1.0 + 0.5, 1.0)

    fig = plt.figure(figsize=(20, 12))  # Augmentation de la taille de la figure pour plus d'espace
    ax = fig.add_subplot(111)

    index = 0
    max_len = []  # Liste pour stocker les longueurs maximales des opérations
    for machine, operations in sorted(data.items()):
        for op in operations:
            max_len.append(op[1])  # Ajoute la fin de l'opération à la liste max_len
            job = op[2].split('-')[0]  # Extrait l'ID du job
            if job not in job_colors:
                # Attribue une nouvelle couleur au job s'il n'a pas encore de couleur
                job_colors[job] = additional_colors[len(job_colors) % len(additional_colors)]
            c = job_colors[job]  # Récupère la couleur du job
            rect = ax.barh((index * 1.0) + 0.5, op[1] - op[0], left=op[0], height=0.4, align='center',
                           edgecolor=c, color=c, alpha=0.8)

            # Ajout de l'étiquette
            width = int(rect[0].get_width())
            Str = "{}".format(op[2])  # Texte de l'étiquette (nom de l'opération)
            xloc = op[0] + 0.50 * width  # Position en x de l'étiquette
            clr = 'black'  # Couleur de l'étiquette
            align = 'center'  # Alignement de l'étiquette

            yloc = rect[0].get_y() + rect[0].get_height() / 2.0  # Position en y de l'étiquette
            # Ajout du texte avec une police plus petite et une orientation verticale
            ax.text(xloc, yloc, Str, horizontalalignment='center',
                    verticalalignment='center', color=clr, weight='bold',
                    clip_on=True, fontsize=8, rotation=90)  # Taille de police plus petite et rotation verticale
        index += 1

    # Définir les limites de l'axe des y
    ax.set_ylim(ymin=-0.1, ymax=nb_row * 1.0 + 0.5)
    # Ajouter une grille
    ax.grid(color='gray', linestyle=':')
    # Définir les limites de l'axe des x
    ax.set_xlim(0, max(10, max(max_len)))

    # Rotation des labels de l'axe des x
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    # Définir les labels de l'axe des y
    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=14)

    # Définir les propriétés de la légende
    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    # Inverser l'axe des y
    ax.invert_yaxis()

    # Ajouter le makespan total au titre
    total_makespan = max(max_len)
    plt.title(f"Flexible Job Shop Solution AG native (Makespan: {total_makespan})")

    # Sauvegarder le diagramme de Gantt
    plt.savefig(filename)
    # Fermer la figure pour éviter de l'afficher
    plt.close(fig)