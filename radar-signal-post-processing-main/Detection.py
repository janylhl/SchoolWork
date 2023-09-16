"""
Implémentation d'un algorithme CFAR à moyenne
@author: Janyl
"""
import numpy as np
import matplotlib.pyplot as plt


def CFAR(signal, nb_entrainement, nb_garde, taux_fa):
    """
    :param signal: Données à traiter
    :param nb_entrainement: Nombre de cellules d'entraînement
    :param nb_garde: Nombre de cellule de garde
    :param taux_fa: Taux de fausse alarme
    :return: liste des pics détéctés
    """

    # Nombre total de cellules
    nb_cellules = signal.size
    # Taille de la zone de gardes à l'avant et à l'arrière de la cellule testée
    nb_garde_demi = round(nb_garde / 2)
    # Taille de zone d'entraînement à l'avant et à l'arrière de la cellule testée
    nb_entrainement_demi = round(nb_entrainement / 2)
    # Taille de la zone de travail à l'avant et à l'arrière de la cellule testée
    nb_cote = nb_garde_demi + nb_entrainement_demi

    # Facteur de seuil
    alpha = nb_entrainement * (taux_fa ** (-1 / nb_entrainement) - 1)

    idx_pics = []
    for i in range(nb_cote, nb_cellules - nb_cote):
        # Vérifie que la cellule considérée n'est pas un extremum local

        if i != i - nb_cote + np.argmax(signal[i - nb_cote:i + nb_cote + 1]):
            continue

        # Somme des valeurs de toutes les cellules entrant de le calcul courant
        somme1 = np.sum(signal[i - nb_cote:i + nb_cote + 1])
        # Somme des valeurs comprises dans la zone de garde
        somme2 = np.sum(signal[i - nb_garde_demi:i + nb_garde_demi + 1])
        # Calcul du bruit en foction des valeurs présentent dans les cellules d'entrainement uniquement
        p_bruit = (somme1 - somme2) / nb_entrainement
        # Calcul de la valeur de seuil
        seuil = alpha * p_bruit

        if (signal[i] > seuil):
            idx_pics.append(i)  # Stockage des indices des pics

    idx_pics = np.array(idx_pics, dtype=int)
    return idx_pics


def MatrixCFAR(Mi, nb_entrainement, nb_garde, taux_fa):
    N = np.shape(Mi)[0]

    lcibles = []
    for i in range(N):
        lsignal = Mi[i]
        lcibles.append(CFAR(lsignal, nb_entrainement, nb_garde, taux_fa))
    Mcibles = np.asarray(lcibles)
    return Mcibles


def plot_Cibles(x, signal, idx_pics):
    print("idx_pics =", idx_pics)
    print(type(signal))
    print(type(idx_pics))
    plt.figure()
    plt.plot(x, signal)
    #plt.plot(x[idx_pics], signal[idx_pics], 'rD')
    for i in range (len(idx_pics)):
        point = idx_pics[i]
        plt.plot(x[point], signal[point], 'rD')
    plt.xlabel('t')
    plt.ylabel('signal')
    plt.title('Cibles detectés')
    plt.show()





