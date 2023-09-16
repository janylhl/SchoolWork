"""
Extarction de distances, position etc...
@author: Janyl
"""
import numpy as np

def distance(cibles, fsamp):
    """
    Détermination des distances cibles - radar
    :param fsamp: frequence d'échantillonnage
    :param cibles: liste des cibles détectées (indices dans la listes du signal reçu)
    :return: distanbances de chaque cible au radar en mètres
    """
    c = 3E8
    Distances = []

    for i in range(len(cibles)):
        T = 1 / fsamp  # Période d'échantillonage
        Dt = cibles[i] * T  # Décallage temporel de l'écho due à la cible
        R = (c * abs(Dt)) / 2  # Distance cible - radar
        Distances.append(R)
    return Distances


def MatrixDistance(Mcibles, fsamp):
    N = np.shape(Mcibles)[0]
    lcibles = Mcibles.tolist()
    ldistances = []
    for i in range(N):
        ldistances.append(distance(lcibles[i], fsamp))
    Mdistances = np.asarray(ldistances)
    #Mdistances.reshape((len(ldistances), len(ldistances[0])))
    #print(type(Mdistances), np.shape(Mdistances))
    return Mdistances


def coordonnees():
    print('soon')
