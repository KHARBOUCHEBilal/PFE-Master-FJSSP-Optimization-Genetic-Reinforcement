#!/usr/bin/env python

# Ce module décide quand l'algorithme génétique doit s'arrêter. Nous utilisons
# uniquement un nombre maximum de générations pour le moment.

from src import config

def shouldTerminate(population, gen):
    """
    Détermine si l'algorithme génétique doit s'arrêter.
    :param population: Liste des individus de la population.
    :param gen: Nombre actuel de générations.
    :return: True si le nombre de générations est supérieur au maximum autorisé, sinon False.
    """
    return gen > config.maxGen

