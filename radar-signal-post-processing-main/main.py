
import numpy as np
from Detection import *
from knn_1D import *
from position import *
from radar import *
from filtrage import *

if __name__ == '__main__':
    """ 1 - Pré traitement / mise en forme du signal """

    # Données d'entrée à fournir
    path = 'data/chirp_perso.txt'
    fsamp = 1500e6
    Trec = 699e-6
    nb_entrainement = 40000
    nb_garde = 10000
    taux_fa = 1e-6

    # Ouverture de fichier
    # x = np.arange(S_recu.size)
    # fe = 9 * 10 ** 9
    # Te = 1 / fe

    # Ouverture, découpage du signal et mise sous forme de matrices

    S_emis, S_recu = load(path)
    #print(type(S_emis))
    MatrixSe = receivedSignalToMatrix(S_emis, fsamp, Trec)
    #print(MatrixSe)
    MatrixSr = receivedSignalToMatrix(S_recu, fsamp, Trec)
    #(MatrixSr)

    """ 2 - Filtrage adapté """

    MatrixSi = correlationMatrix(MatrixSe, MatrixSr)
#print(MatrixSi)


    """ 3 - Detection """

    MatrixCibles = MatrixCFAR(MatrixSi, nb_entrainement, nb_garde, taux_fa)
    print(type(MatrixCibles))
    plot_Cibles(list(range(len(MatrixSi[0].tolist()))), MatrixSi[0].tolist(), MatrixCibles[0].tolist())

    """ 4 - Extraction de la localisation"""

    MatrixDistances = MatrixDistance(MatrixCibles, fsamp)
    print(MatrixDistances)

    """ 5 - Tracking """
    jeu_test = MatrixDistances

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
