# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 13:33:22 2020

@author: emili
"""

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import sqrtm, expm, norm, block_diag

"""Mise en place des 2 aspects de correction et de prédiction nécessaires pour pouvoir 
ensuite implémenter le filtre de kalman"""


# prediction

def kalman_predict(xk, gammak, u, gamma_alpha, A):
    gammak_suiv = A @ gammak @ (A.T) + gamma_alpha
    x_suiv = A @ xk + u
    return gammak_suiv, x_suiv


def kalman_correc(x0, gamma0, y, gamma_beta, C):
    S = np.dot(np.dot(C, gamma0), (C.T)) + gamma_beta
    K = gamma0 @ (C.T) @ (np.linalg.inv(S))
    y_tilde = y - C @ x0
    gammak = (np.eye(len(x0)) - K @ C) @ gamma0
    xk = x0 + K @ y_tilde
    return xk, gammak


"""implémentation du filtre de kalman"""


def kalman(x0, gamma0, u, y, gamma_alpha, gamma_beta, A, C):
    """retourne x_instant_suivant et gamma_x_instant_suivant"""
    xk, gammak = kalman_correc(x0, gamma0, y, gamma_beta, C)
    gamma_suivant, x_suivant = kalman_predict(xk, gammak, u, gamma_alpha, A)
    return x_suivant, gamma_suivant


"""tracé des ellipses de confiance autour de chaque point calculé par le filtre de kalman"""


def tracer_ellipse(c, gamma, eta, ls):
    s = np.arange(0, 2 * np.pi, 0.001)
    w = c * np.ones(s.shape) + np.dot(sqrtm(-2 * np.log(1 - eta) * gamma), np.array([np.cos(s), np.sin(s)]))
    plt.plot(w[0, :], w[1, :], linestyle=ls)


"""exemple d'utilisation de l'algorithme

on rappelle que les équations d'état du système sont :
    équation d'évolution : x(k+1) = A*x(k) + u + alpha
    équation d'observation : y(k) = C*x(k) + beta

x_chap0 : valeur de départ fournie par l'algorithme de détection
gamma0 : précision sur x_chap0
u : commande du système
y : mesure 
gamma_alpha : matrice de covariance / bruit
gamma_beta : matrice de covariance / bruit de mesure 
A : matrice du sytème (évolution)
C : matrice (observation)

#execution de l'algorithme en une seule fois 

plt.figure()
x_chap, gamma = kalman(x_chap0, gamma0, u, y, gamma_alpha, gamma_beta, A, C)
tracer_ellipse(x_chap, gamma, 0.99, '-')
plt.plot()
"""
