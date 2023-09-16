import numpy as np
import math as m
import matplotlib.pyplot as plt

"""on fait de la dimension 1. Utilisation de l'axe des x"""


def distance_eucl(donnee, d):
    """donnée : [y] (pas de prise en compte des x) c'est la distance au radar placé en 0 et d : liste de data de la forme [y, classe], data étant une liste de listes des données déjà traitées et disponibles
    renvoit pour chaque point du set de donnée la distance au nouveau plot en position y selon
    distance < 0 : le point est plus loin sur l'axe
    distance > 0 : le point est plus proche"""
    distance = 0.0
    distance = distance + (donnee[0] - d[0])
    return distance


def calcul_seuil(vitesse, duree):
    """calcul du seuil pour l'algorithme suivant la vitesse de déplacement de l'objet et le temps entre
    2 acquisitions (on fait les mesures en "discret")
    si la distance est supérieure au seuil : l'objet se déplace plus vite que celui traqué ou il s'agit d'un objet totalement different
    il y a de forte chance que se soit une autre cible """
    seuil = (vitesse * duree) + 2  # données parfaites
    # seuil = 0.01 # acquisition réelle
    return seuil


def trouver_voisins(data, donnee, nb_voisins):
    """data: liste : ensemble de donnee à tester, d in data est de la forme [y,piste]
    donnee est la donnée testée de la forme [y]
    nb_voisins = k = nb de voisins souhaités
    on gère aussi la création d'une nouvelle piste si les distance aux k plus proches voisins sont trop grandes
     c'est dans cette fonction que l'on définit le seuil"""
    distances = []
    for d in data:
        dist = distance_eucl(donnee, d)
        distances.append((d, dist))
    # tri
    distances.sort(key=lambda tup: tup[1])
    voisins = []

    # vérification distances # on change le seuil ici !
    seuil = calcul_seuil(10000, 150000)
    cpt = 0
    for i in range(nb_voisins):
        if np.abs(distances[i][1]) > seuil:
            cpt += 1
    if cpt == nb_voisins:
        print("le plot n'appartient à aucune piste, on en crée une nouvelle")
    else:
        for i in range(nb_voisins):
            voisins.append(distances[i][0])

    # création listes des k plus proches voisins : à décommenter si on ne fait pas la vérification de distances
    # for i in range(nb_voisins):
    # voisins.append(distances[i][0])

    # on renvoit les k plus proches voisins de la donnée testée
    return voisins


def prediction_classe(data, donnee, nb_voisins):
    """data: liste : ensemble de donnee à tester, d in data est de la forme [y,piste]
        donnee est la donnée testée de la forme [y]
        nb_voisins = k = nb de voisins souhaités"""
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
    # data = []
    radar = [25000]  # position de l'observateur

    # visualisation
    plt.figure()
    plt.subplot(211)
    plt.plot(piste[0][0], 'bo', color='blue', label="piste")
    for i in range(1, len(piste)):
        plt.plot(piste[i - 1][0], color='blue')
        plt.plot(piste[i][0], 'bo', color='blue')

    plt.plot(donnee[0], 'bo', color="green", label="plot à tester")
    plt.plot(radar[0], 'bo', color="yellow", label="radar")
    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N")
    # fin visualisation

    # prediction
    classe_donnee = prediction_classe(piste, donnee, k)

    # nouvelle piste au cas ou on en ait besoin
    piste_nvx = []

    if classe_donnee != 100:
        print("le plot appartient à la piste")
        donnee.append(classe_donnee)
        piste.append(donnee)
        distance_cible_radar = distance_eucl(donnee, radar)
        distance_donne_precedent = distance_eucl(donnee, piste[-2])

        print("piste mise à jour:", piste)
        print("le nouveau point est à :", distance_cible_radar, "m du radar")
        print("le point c'est déplacé de:", distance_donne_precedent,
              "m entre son emplacement précédent et son emplacement actuel")

        # visualisation
        plt.subplot(212)
        plt.plot(piste[0][0], 'bo', color='blue', label="piste")
        for i in range(1, len(piste)):
            plt.plot(piste[i - 1][0], color='blue')
            plt.plot(piste[i][0], 'bo', color='blue')
        plt.plot(radar[0], 'bo', color="yellow", label="radar")
        plt.legend()
        plt.grid()
        plt.xlabel("abs")
        plt.ylabel("ordonnées")
        plt.title("situation N+1")

    else:
        # on traite les cas divergents ici
        # on crée la nouvelle piste, on oublie pas de gérer un eventuel drop.
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
        plt.plot(piste[0][0], 'bo', color='blue', label="piste")
        plt.plot(piste_nvx[0][0], 'bo', color='red', label="nouvelle piste")
        for i in range(1, len(piste)):
            plt.plot(piste[i - 1][0], color='blue')
            plt.plot(piste[i][0], 'bo', color='blue')
        plt.plot(radar[0], 'bo', color="yellow", label="radar")
        plt.legend()
        plt.grid()
        plt.xlabel("abs")
        plt.ylabel("ordonnées")
        plt.title("situation N+1")

    plt.show()
    return piste, piste_nvx, distance_donne_precedent


def suivi_2_cible(donnee, k, piste_1, piste_2):
    """Algo pour suivi de 2 cible
        entrées :
        donnee : plot à tester
        k : nombre de voisins souhaités
        piste_1 : piste de la première cible
        piste_2 : piste de la deuxieme cible
        sortie :
        pistes 1 et 2 mises à jours et distance du plot au radar et au point précédent de sa piste"""

    data = []
    nb_piste = 2
    check = []
    radar = [25000]

    # création du jeu de données sur lequel on applique l'algo knn
    data.extend(piste_1)
    data.extend(piste_2)

    check = check + [piste_1] + [piste_2]

    # visualisation situation de depart
    plt.figure()
    plt.subplot(211)
    plt.plot(piste_1[0][0], 'bo', color='blue', label="piste 1")
    plt.plot(piste_2[0][0], 'bo', color='red', label="piste 2")
    for i in range(1, len(piste_1)):
        plt.plot(piste_1[i - 1][0], color='blue')
        plt.plot(piste_1[i][0], 'bo', color='blue')
    for i in range(1, len(piste_2)):
        plt.plot(piste_2[i - 1][0], color='red')
        plt.plot(piste_2[i][0], 'bo', color='red')

    plt.plot(donnee[0], 'bo', color="green", label="pt à tester")
    plt.plot(radar[0], 'bo', color="yellow", label="radar")

    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N")
    # fin visualisation

    classe_donnee = prediction_classe(data, donnee, k)
    piste_nvx_2 = []
    print("le plot appartient à la piste:", classe_donnee)

    if classe_donnee == 100:
        print("initialisation nouvelle piste")
        distance_donne_precedent = 0
        donnee.append(3)
        piste_nvx_2 = [donnee]
        print("nouvelle piste:", piste_nvx_2)
    else:
        piste_nvx_2 = []

    # ajout à la piste correspondante et mise à jour des pistes
    for i in range(1, 35):
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
    print("le point s'est déplacé de:", distance_donne_precedent,
          "m entre son emplacement précédent et son emplacement actuel")

    # visualisation après méthode des knn
    plt.subplot(212)
    plt.plot(piste_1[0][0], 'bo', color='blue', label="piste 1")
    plt.plot(piste_2[0][0], 'bo', color='red', label="piste 2")
    plt.plot(radar[0], 'bo', color='yellow', label="radar")
    if piste_nvx_2 != []:
        plt.plot(piste_nvx_2[0][0], 'bo', color='black', label="nouvelle piste")
        for i in range(1, len(piste_1)):
            plt.plot(piste_1[i - 1][0], color='blue')
            plt.plot(piste_1[i][0], 'bo', color='blue')
        for i in range(1, len(piste_2)):
            plt.plot(piste_2[i - 1][0], color='red')
            plt.plot(piste_2[i][0], 'bo', color='red')

    else:
        for i in range(1, len(piste_1)):
            plt.plot(piste_1[i - 1][0], color='blue')
            plt.plot(piste_1[i][0], 'bo', color='blue')
        for i in range(1, len(piste_2)):
            plt.plot(piste_2[i - 1][0], color='red')
            plt.plot(piste_2[i][0], 'bo', color='red')

    plt.legend()
    plt.grid()
    plt.xlabel("abs")
    plt.ylabel("ordonnées")
    plt.title("situation N+1")
    plt.show()
    # fin visualisation
    return piste_1, piste_2, piste_nvx_2


def un_tour_2_cibles(nb_iter, piste_1, piste_nvx, liste_donnees, n, cpt_1, cpt_2, k):
    if nb_iter >= 0:

        print(n + 1, "ème tour avec 2 pistes")
        # suivi de 2 cibles
        piste_1_prec = piste_1
        piste_2_prec = piste_nvx
        piste_1, piste_nvx, nouvelle_piste, = suivi_2_cible(liste_donnees[n], k, piste_1, piste_nvx)
        print("piste 1 updated 2eme tour", piste_1)
        print("nouvelle piste initialisée", piste_nvx)
        print("une troisième piste ?", nouvelle_piste)

        # test si oui ou non drop
        if piste_1_prec == piste_1:
            cpt_1 += 1
            if cpt_1 == 4:
                print("la piste 1 n'a pas été mise à jour depuis 4 tours : DROP")

        if piste_2_prec == piste_2:
            cpt_2 += 1
            if cpt_2 == 4:
                print("la piste 2 n'a pas été mise à jour depuis 4 tours : DROP")

        piste_1_prec = piste_1
        piste_2_prec = piste_nvx

        nb_iter = nb_iter - n
        n += 1

        return nb_iter, piste_1, piste_nvx, liste_donnees, n, cpt_1, cpt_2, nouvelle_piste

    else:
        print("plus de données")


def un_tour_1_cible(nb_iter, piste_1, liste_donnees, n, k):
    if nb_iter >= 0:
        # on a 1 piste
        print(n + 1, "ème tour avec 1 piste")
        piste_1, piste_nvx, _ = suivi_1_cible(liste_donnees[n - 1], piste_1, k)
        print("piste 1 updated", piste_1)
        print("une deuxième piste ?", piste_nvx)

        nb_iter = nb_iter - n
        n += 1

        return nb_iter, piste_1, liste_donnees, n, piste_nvx

    else:
        print("plus de données")


def algo_knn(piste_1, liste_donnees, k):
    """on suit l'objet qui a laissé piste_1 comme trace
    liste_donnees est la liste de toutes les données récupérées et traitées après acquisition"""

    nb_iter = len(liste_donnees)
    cpt_1 = 0
    cpt_2 = 0
    n = 0
    print("on effectue ", nb_iter, " tours d'algo")
    print("let's start")

    nb_iter, piste_1, liste_donnees, n, piste_nvx = un_tour_1_cible(nb_iter, piste_1, liste_donnees, n, k)

    if n < nb_iter:
        # différenciation des cas : 1 ou 2 pistes
        if piste_nvx:
            # on a initialisé une 2eme piste
            nb_iter, piste_1, piste_nvx, liste_donnees, n, cpt_1, cpt_2, _ = un_tour_2_cibles(nb_iter, piste_1,
                                                                                              piste_nvx,
                                                                                              liste_donnees, n, cpt_1,
                                                                                              cpt_2, k)


        else:
            nb_iter, piste_1, liste_donnees, n, piste_nvx = un_tour_1_cible(nb_iter, piste_1, liste_donnees, n, k)

    return piste_1, piste_nvx


if __name__ == "__main__":
    donnee = [4]
    donnee_2 = [4.1]
    data = [[39982.54], [39982.44]]
    data_2 = [[39982.74], [39982.964], [39992.964]]

    # on suppose que les pistes sont "triées" dans l'ordre d'apparition des plots dans cette dernière
    jeu_test = [list([26832.1, 62832.1, 65832.09999999999, 104832.1, 145332.0, 179831.59999999998, 182831.6, 185831.6]),
                list([25332.600000000002, 28332.600000000002, 64332.3, 67332.3, 100332.0, 104832.1, 143831.8, 146831.5,
                      182831.19999999998, 185831.19999999998])]
    print(jeu_test[0])

    piste_2 = [[2, 2],
               [4.5, 2],
               [6, 2],
               [7, 2],
               [8, 2]]

    piste_3 = [[0.5, 3],
               [1, 3],
               [1.5, 3],
               [3, 3],
               [4, 3]]

    # piste_4 = [[39982, 4]]
    # piste_maj, piste_nvx = algo_knn(piste_4, data, 1)
    # print(piste_maj)
    # for i in range(0, len(data_2)):
    #     print(i)
    #     piste_maj, piste_nvx = algo_knn(piste_maj, [data_2[i]], 3)
    #
    # print(piste_maj)

    piste_test = [[jeu_test[0][0], 6]]
    data_t = [[jeu_test[0][1]], [jeu_test[0][2]]]
    data_2_t = []
    for i in range(3, len(jeu_test[0])):
        data_2_t.append([jeu_test[0][i]])

    print(data_2_t)

    piste_maj_test, piste_nvx_t = algo_knn(piste_test, data_t, 1)

    for i in range(0, len(data_2_t)):
        piste_maj_test, piste_nvx = algo_knn(piste_maj_test, [data_2_t[i]], 3)

    print(piste_maj_test)
