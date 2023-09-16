# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:14:32 2020

@author: emili
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

"""algorithme des k plus proches voisins pour la prédiction de la prochaine position de la cible.
tracking
ce fait en 3 étapes :
    - calcul de la distance aux autres points : ici distance euclidienne
    - identifier les plus proches voisins
    - prédiction"""

"""calcul de la distance euclidienne
on met les données à tester sous la forme : data = [[x0,y0,classe],[x1,y1, classe],...]
classe représente la piste à laquelle appartient la donnée (1 piste = 1 classe)
On renvoit "distance" : plus cette valeur est petite, plus les données sont similaires
on pose donnee = data[0]
on boucle :
    for d in data :
        distance = distance_eucl(donnee,d)"""


# à faire : trouver une fonction qui discrimine et permet de commencer une nouvelle piste si les points ne correspondent pas
# on impose un seuil (dépend à priori de ce qu'on eut observer, au-delà de cette distance : nouvelle piste


def distance_eucl(donnee, d):
    """donnée du type liste [x,y] et data du type liste [x, y, classe]"""
    distance = 0.0
    distance = distance + (d[0] - donnee[0]) ** 2 + (d[1] - donnee[1]) ** 2
    return m.sqrt(distance)


"""on a donc calculé la distance du nouveau point aux autres points déjà relevé
on détermine les k plus proches voisins du nouveau point data[0] à l'aide d'un fonction de tri
trouver_voisins(data,data[0],k)"""


def trouver_voisins(data, donnee, nb_voisins):
    """data: liste : ensemble de donnee à tester, d in data est de la forme [x,,y,piste]
    donnee est la donnée testée de la forme [x, y]
    nb_voisins = k = nb de voisins souhaités
    on gère aussi la création d'une nouvelle piste si les distance aux k plus proches voisins sont trop grandes """
    distances = []
    for d in data:
        dist = distance_eucl(donnee, d)
        distances.append((d, dist))
    # tri
    distances.sort(key=lambda tup: tup[1])
    voisins = []

    # vérification distances
    seuil = 5
    cpt = 0
    for i in range(nb_voisins):
        if distances[i][1] > seuil:
            cpt += 1
    if cpt == nb_voisins:
        print("le plot n'appartient à aucune piste, on en crée une nouvelle")
    else:
        for i in range(nb_voisins):
            voisins.append(distances[i][0])

    # création listes des k plus proches voisins : à décommenter si on ne fait pas la vérification de distances
    #for i in range(nb_voisins):
        #voisins.append(distances[i][0])

    # on renvoit les k plus proches voisins de la donnée testée
    print("voisins:", voisins)
    return voisins


"""prédiction à effectuer : on fonctionne avec des classes
Une classe = une piste ie trajectoire
On cherche à quelle classe ajouter le nouveau points data[0]"""


def prediction_classe(data, donnee, nb_voisins):
    voisins = trouver_voisins(data, donnee, nb_voisins)
    if not voisins:
        print("nouvelle affectation")
        prediction = 100
    else:
        output = [d[-1] for d in voisins]
        prediction = max(set(output), key=output.count)

    return prediction


def ajout(data, donnee, classe_donnee):
    """on ajoute la donnée à la bonne piste"""
    donnee.append(classe_donnee)
    data.append(donnee)
    return data


def suivi_1_cible(donnee, piste, k):
    """on se donne en entrée la donnée à tester. On ne suit qu'une seule cible. il faut mettre en place une
    discrimination pour pouvoir créer une nouvelle piste si un plot est loin par rapport à un seuil déterminé il faut
    aussi pouvoir dropper cette piste si on ne détecte pas d'autre plots autour de ce dernier dans les 3 prochaines
    acquisitions """
    #data = []
    radar = [0, 0]

    # visualisation
    plt.figure()
    plt.subplot(211)
    plt.plot(piste[0][0], piste[0][1], 'bo', color='blue', label="piste")
    for i in range(1, len(piste)):
        plt.plot([piste[i - 1][0], piste[i][0]], [piste[i - 1][1], piste[i][1]], color='blue')
        plt.plot(piste[i][0], piste[i][1], 'bo', color='blue')

    plt.plot(donnee[0], donnee[1], 'bo', color="green", label="plot à tester")
    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N")
    # fin visualisation

    # prediction
    classe_donnee = prediction_classe(piste, donnee, k)

    # nouvelle piste au cas ou on en ait besion
    piste_nvx = []

    if classe_donnee != 100:
        print("le plot appartient à la piste")
        donnee.append(classe_donnee)
        piste.append(donnee)
        distance_donne_precedent = distance_eucl(donnee, piste[-2])
        distance_cible_radar = distance_eucl(donnee, radar)

        print("piste mise à jour:", piste)
        print("le nouveau point est à :", distance_cible_radar, "m du radar")
        print("le point c'est déplacé de:", distance_donne_precedent,"m entre son emplacement précédent et son emplacement actuel")

        # visualisation
        plt.subplot(212)
        plt.plot(piste[0][0], piste[0][1], 'bo', color='blue', label="piste")
        for i in range(1, len(piste)):
            plt.plot([piste[i - 1][0], piste[i][0]], [piste[i - 1][1], piste[i][1]], color='blue')
            plt.plot(piste[i][0], piste[i][1], 'bo', color='blue')
        plt.legend()
        plt.grid()
        plt.xlabel("abs")
        plt.ylabel("ordonnées")
        plt.title("situation N+1")

    else :
        #on traite les cas divergents ici
        #on crée la nouvelle piste, on oublie pas de gérer un eventuel drop.
        print("le plot n'appartient pas à la piste")
        donnee.append(34)
        print("la nouvelle piste associée porte le numéro 34")
        piste_nvx.append(donnee)
        distance_donne_precedent = 0
        distance_cible_radar = distance_eucl(donnee, radar)

        print("nouvelle piste:", piste_nvx, "\n piste :", piste)
        print("le nouveau point est à :", distance_cible_radar, "m du radar")

        # visualisation
        plt.subplot(212)
        plt.plot(piste[0][0], piste[0][1], 'bo', color='blue', label="piste")
        plt.plot(piste_nvx[0][0], piste_nvx[0][1], 'bo', color='red', label="nouvelle piste")
        for i in range(1, len(piste)):
            plt.plot([piste[i - 1][0], piste[i][0]], [piste[i - 1][1], piste[i][1]], color='blue')
            plt.plot(piste[i][0], piste[i][1], 'bo', color='blue')
        plt.legend()
        plt.grid()
        plt.xlabel("abs")
        plt.ylabel("ordonnées")
        plt.title("situation N+1")


    plt.show()

"""Data est créee par concaténation de liste, 1 liste = 1 classe = 1 piste 
on renvoit les différentes listes mises à jours puis pour le point testé on renvoit sa piste et sa distance à l'observateur 
on suppose obs = [0,0] (position du radar i.e de l'observateur) """


def suivi_2_cible(donnee, k, piste_1, piste_2):
    """Algo pour suivi de 2 cible
        entrées :
        donnee : plot à tester
        k : nombre de voisins souhaités
        piste_1 : piste de la première cible
        piste_2 : piste de la deuxieme cible
        sortie :
        pistes 1 et 2 mises à jours et distance du plot au radar et au point précédent de sa piste"""
    global piste_nvx
    data = []
    nb_piste = 2
    check = []
    radar = [0, 0]

    # création du jeu de données sur lequel on applique l'algo knn
    data.extend(piste_1)
    data.extend(piste_2)

    check = check + [piste_1] + [piste_2]

    # visualisation situation de depart
    plt.figure()
    plt.subplot(211)
    plt.plot(piste_1[0][0], piste_1[0][1], 'bo', color='blue', label="piste 1")
    plt.plot(piste_2[0][0], piste_2[0][1], 'bo', color='red', label="piste 2")
    for i in range(1, len(piste_1)):
        plt.plot([piste_1[i - 1][0], piste_1[i][0]], [piste_1[i - 1][1], piste_1[i][1]], color='blue')
        plt.plot(piste_1[i][0], piste_1[i][1], 'bo', color='blue')
    for i in range(1, len(piste_2)):
        plt.plot([piste_2[i - 1][0], piste_2[i][0]], [piste_2[i - 1][1], piste_2[i][1]], color='red')
        plt.plot(piste_2[i][0], piste_2[i][1], 'bo', color='red')

    plt.plot(donnee[0], donnee[1], 'bo', color="green", label="pt à tester")

    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N")
    # fin visualisation

    classe_donnee = prediction_classe(data, donnee, k)
    piste_nvx = []
    print("le plot appartient à la piste:", classe_donnee)

    if classe_donnee == 100:
        print("initialisation nouvelle piste")
        distance_donne_precedent = 0
        donnee.append(3)
        piste_nvx = [donnee]
        print("nouvelle piste:", piste_nvx)

    # ajout à la piste correspondante et mise à jour des pistes
    for i in range(1, nb_piste + 1):
        if classe_donnee == i:
            # on ajoute le point à la piste correspondante
            donnee.append(classe_donnee)
            check[i - 1].append(donnee)
            distance_donne_precedent = distance_eucl(donnee, check[i - 1][-2])
            print(check)

    piste_1 = check[0]
    piste_2 = check[1]

    print("piste 1 :", piste_1)
    print("piste 2 :", piste_2)

    distance_cible_radar = distance_eucl(donnee, radar)

    print("le nouveau point est à :", distance_cible_radar, "m du radar")
    print("le point c'est déplacé de:", distance_donne_precedent,
          "m entre son emplacement précédent et son emplacement actuel")

    # visualisation après méthode des knn
    plt.subplot(212)
    plt.plot(piste_1[0][0], piste_1[0][1], 'bo', color='blue', label="piste 1")
    plt.plot(piste_2[0][0], piste_2[0][1], 'bo', color='red', label="piste 2")
    if piste_nvx:
        plt.plot(piste_nvx[0][0], piste_nvx[0][1], 'bo', color='black', label="nouvelle piste")

    for i in range(1, len(piste_1)):
        plt.plot([piste_1[i - 1][0], piste_1[i][0]], [piste_1[i - 1][1], piste_1[i][1]], color='blue')
        plt.plot(piste_1[i][0], piste_1[i][1], 'bo', color='blue')
    for i in range(1, len(piste_2)):
        plt.plot([piste_2[i - 1][0], piste_2[i][0]], [piste_2[i - 1][1], piste_2[i][1]], color='red')
        plt.plot(piste_2[i][0], piste_2[i][1], 'bo', color='red')

    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N+1")
    plt.show()
    # fin visualisation


if __name__ == "__main__":
    donnee = [5, 5]
    donnee_eclatee_au_sol = [-20, -20]
    k = 3  # nombre de voisins souhaité
    piste_1 = [[7, 7, 1],
               [8, 7, 1],
               [1, 2, 1],
               [-2, 2, 1],
               [2, 2, 1]
               ]
    piste_2 = [[2, 1.8, 2],
               [6, 5, 2],
               [8, 6, 2],
               [6, 6.4, 2],
               [0, 3, 2]]

    piste_3 = [[0, 2, 3],
               [1, 3, 3],
               [1.5, 4, 3],
               [3, 2, 3],
               [4, 3, 3]]

    #suivi_2_cible(donnee, k, piste_1, piste_2)
    suivi_1_cible(donnee_eclatee_au_sol, piste_3,3)

