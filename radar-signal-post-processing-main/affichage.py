import numpy as np
import matplotlib.pyplot as plt


def affiche_signal(Te, Ne, u0, u01):
    # Le signal est échantillonné sur une durée T plus grande que sa période
    #le zero-padding n'apporte pas une plus grande précision spectrale
    t0 = np.arange(0, Te * Ne, Te)
    t01 = np.arange(0, 201*Te * Ne, Te)

    plt.figure()
    plt.title('Affichage du Signal')
    plt.xlabel('t (s)')
    plt.ylabel('u (V)')
    plt.grid()
    #plt.plot(t0,u0[:Ne])
    plt.plot(t0, u0)
    plt.show()
    #affichage du signal avec zero-padding
    plt.plot(t01, u01)
    plt.title('Affichage du Signal avec zero-padding')
    plt.show()
    #Graphe de barres verticales par le point à la coordonnée indiquée
    #plt.stem(t0, u0,use_line_collection=True)
    """plt.xlabel('t')
    plt.ylabel('u')
    plt.title('Affichage du signal en barres verticales')
    plt.grid()
    plt.show()"""

def affiche_spectre_zoom(Te, Ne, u0):
    #spectre=np.absolute(np.fft.fft(u0))/(10*Ne)
    #frequences = np.arange(0, 10 * fe, fe / Ne)
    spectre = np.absolute(np.fft.fft(u0)) *2/ Ne
    #frequences=np.arange(-fe/2,fe/2,fe/Ne)
    n=u0.size
    frequences=np.fft.fftfreq(n,Te)
    plt.figure()
    plt.plot(frequences,spectre)
    plt.title('Zoom du Spectre sur les harmoniques')
    plt.xlabel('f (Hz)')
    plt.ylabel('A')
    plt.grid()
    #plt.axis([-0.1*10**9,1.5*10**10,-0.02,0.05])
    plt.axis([-1 * 10 * 9, 1 * 10 * 9, -0.1, 0.4])


def affiche_spectre(Te, Ne, u0, u01):
    #spectre = np.absolute(np.fft.fft(u0)) / (10*Ne)
    #frequences = np.arange(0,10*fe, fe / Ne)
    #frequences = np.arange(-fe/2, fe/2, fe / Ne)
    n = u0.size
    frequences = np.fft.fftfreq(n, Te)
    spectre = np.absolute(np.fft.fft(u0))*2 / Ne
    plt.figure()
    plt.plot(frequences, spectre)
    plt.title('Affichage du spectre')
    plt.xlabel('f (Hz)')
    plt.ylabel('A')
    plt.grid()
    plt.show()
    """plt.title('Affichage du spectre en barres verticales')
    plt.stem(frequences, spectre, use_line_collection=True)
    plt.show()"""
    n = u01.size
    frequences1 = np.fft.fftfreq(n, 201*Te)
    spectre1 = np.absolute(np.fft.fft(u01)) * 2 / Ne
    plt.figure()
    plt.plot(frequences1, spectre1)
    plt.title('Affichage du spectre avec zero-padding')
    plt.show()

