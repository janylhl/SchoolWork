"""
Created on Thu May  6 15:37:55 2021

@author: leila
"""
import numpy as np
from abc import abstractmethod
import matplotlib.pyplot as plt

"""
Création d'une classe Bateau qui regroupe chaque navire hybride
Avec calcul de résistance à l'avancement + appendices (commun à chaque navire)
"""


class Bateau:
    """on définit les attributs du bateau (les paramètres de celui-ci)"""

    def __init__(self, Lpp, Lwl, B, Tf, Ta, Abt, At, Cstern, Cp, Cm, Cwp, lcb, displacement, hb,
                 S_rudder_behind_skeg, S_rudder_behind_stern, S_twin_screw_balance_rudders, S_shaft_brackets, S_skeg,
                 S_strut_bossing,
                 S_hull_bossings, S_shafts, S_stabilizer_fins, S_dome, S_bilge_keels, D, X_cos, Y_cos, Z_cos, X_0cos,
                 Y_0cos, Z_0cos,
                 Cl_saf, Cd_saf, S_saf, X_cod, Y_cod, Z_cod, X_0cod, Y_0cod, Z_0cod, Cl_deriv, Cd_deriv, S_deriv, GMt,
                 GMl):
        # attribut du bateau
        self.Lpp = Lpp
        self.Lwl = Lwl
        self.B = B
        self.Tf = Tf
        self.Ta = Ta
        self.Abt = Abt
        self.At = At
        self.Cstern = Cstern
        # coefficient de forme
        self.Cp = Cp
        self.Cm = Cm
        self.Cwp = Cwp
        self.lcb = lcb
        self.displacement = displacement
        self.hb = hb
        # surface des appendices pour holltrop
        self.S_rudder_behind_skeg = S_rudder_behind_skeg
        self.S_rudder_behind_stern = S_rudder_behind_stern
        self.S_twin_screw_balance_rudders = S_twin_screw_balance_rudders
        self.S_shaft_brackets = S_shaft_brackets
        self.S_skeg = S_skeg
        self.S_strut_bossing = S_strut_bossing
        self.S_hull_bossings = S_hull_bossings
        self.S_shafts = S_shafts
        self.S_stabilizer_fins = S_stabilizer_fins
        self.S_dome = S_dome
        self.S_bilge_keels = S_bilge_keels
        self.D = D

        # attribut pour le safran
        # coordonnées du point où les forces hydro se concentre sur le safran
        self.X_cos = X_cos
        self.Y_cos = Y_cos
        self.Z_cos = Z_cos
        # coordonnées de l'origine du repère apendice dans celui du bateau
        self.X_0cos = X_0cos
        self.Y_0cos = Y_0cos
        self.Z_0cos = Z_0cos
        self.Cl_saf = Cl_saf
        self.Cd_saf = Cl_saf
        self.S_saf = S_saf

        # attribut pour la derive
        # coordonnées du point où les forces hydro se concentre sur le derive
        self.X_cod = X_cod
        self.Y_cod = Y_cod
        self.Z_cod = Z_cod
        # coordonnées de l'origine du repère dérive dans celui du bateau
        self.X_0cod = X_0cod
        self.Y_0cod = Y_0cod
        self.Z_0cod = Z_0cod
        self.Cl_deriv = Cl_deriv
        self.Cd_deriv = Cl_deriv
        self.S_deriv = S_deriv

        # atribut pour la stabilité
        self.GMt = GMt
        self.GMl = GMl

    def Resistance_avancement(self, V):
        Re = (abs(V * 0.514) * self.Lwl) / nu  # calcul nombre de Reynolds
        Cf = (0.075 / ((np.log10(Re) - 2) ** 2))  # calcul coefficient de frottement
        Fn = ((abs(V * 0.514)) / (np.sqrt(self.Lwl * g)))  # nbr de Froude
        # print('Fn=',Fn)

        if self.Abt == 0:
            FnT = 0
        else:
            FnT = (abs(V * 0.514) / np.sqrt((2 * g * self.At) / (
                        self.B + self.B * self.Cwp)))  # nbr de froude lié à l'immersion du tableau arrière du navire
            # print('Fnt=',FnT)
        Fni = (abs(V * 0.514)) / (np.sqrt(g * (self.Tf - self.hb - (0.25 * np.sqrt(self.Abt))) + 0.15 * (
                    (abs(V * 0.514)) ** 2)))  # nbr de froude lié à l'immersion du navire
        # print('Fni=',Fni)

        d = -0.9

        immerged_volume = self.displacement / rho_eau  # volume immergé
        # print('immerged_volume=',immerged_volume)

        T_average = (np.add(self.Tf, self.Ta)) / 2  # tirant d'eau moyen
        Cb = (self.displacement / rho_eau) / (self.Lwl * self.B * T_average)  # coefficient bloc
        # print('Cb=',Cb)

        Lr = self.Lwl * (1 - self.Cp + ((0.06 * self.Cp * (self.lcb / 100)) / ((4 * self.Cp) - 1)))
        # print('Lr=',Lr)

        Ie = 1 + (89 * (np.exp((-(self.Lwl / self.B) ** 0.80856) * ((1 - self.Cwp) ** 0.30484) * (
                    (1 - self.Cp - (0.0225 * (self.lcb / 100))) ** 0.6367) * ((Lr / self.B) ** 0.34574) * (
                                           ((100 * immerged_volume) / (self.Lwl ** 3)) ** 0.16302))))
        # print('Ie=',Ie)

        # lambda
        if (self.Lwl / self.B) < 12:
            lambd = 1.446 * self.Cp - 0.03 * (self.Lwl / self.B)
        else:
            lambd = (1.446 * self.Cp) - 0.36
        # print('lambd=',lambd)

        WS = self.Lwl * ((2 * T_average) + self.B) * np.sqrt(self.Cm) * (
                    0.453 + (0.4425 * Cb) - (0.2862 * self.Cm) - (0.003467 * (self.B / T_average)) + (
                        0.3696 * self.Cwp)) + (2.38 * (self.Abt / Cb))  # surface mouillée
        # print('WS=',WS)

        if (self.B / self.Lwl) < 0.11:
            c7 = 0.229577 * ((self.B / self.Lwl) ** 0.33333)
        elif (self.B / self.Lwl) < 0.25 and (self.B / self.Lwl) > 0.11:
            c7 = self.B / self.Lwl
        else:
            c7 = 0.5 - 0.0625 * (self.Lwl / self.B)
        # print('c7=',c7)
        c3 = (0.56 * (self.Abt ** 1.5)) / (self.B * T_average * ((0.31 * np.sqrt(self.Abt)) + self.Tf - self.hb))
        # ♠print('c3=',c3)
        c1 = 2223105 * (c7 ** 3.78613) * ((T_average / self.B) ** 1.07961) * ((90 - Ie) ** (-1.37565))
        # print('c1=',c1)
        c2 = np.exp(-1.89 * (np.sqrt(c3)))
        # print('c2=',c2)
        c5 = 1 - ((0.8 * self.At) / (self.B * T_average * self.Cm))
        # print('c5=',c5)
        if FnT < 5:
            c6 = 0.2 * (1 - 0.2 * FnT)
        else:
            c6 = 0
        # print('c6=',c6)
        if (T_average / self.Lwl) < 0.02:
            c12 = 0.479948
        elif (T_average / self.Lwl) < 0.05 and (T_average / self.Lwl) > 0.02:
            c12 = (48.20 * (((T_average / self.Lwl) - 0.02) ** 2.078)) + 0.479948
        else:
            c12 = (T_average / self.Lwl) ** 0.2228446
        # print('c12=',c12)
        c13 = 1 + 0.003 * self.Cstern
        # print('c13=',c13)
        if self.Cp < 0.80:
            c16 = 8.07981 * self.Cp - (13.8673 * (self.Cp ** 2)) + (6.984388 * (self.Cp ** 3))
        else:
            c16 = 1.73014 - 0.7067 * self.Cp
        # print('c16=',c16)
        if ((self.Lwl ** 3) / immerged_volume) < 512:
            c15 = -1.69385
        elif ((self.Lwl ** 3) / immerged_volume) < 512 and ((self.Lwl ** 3) / self.displacement) > 1727:
            c15 = -1.69385 + (((self.Lwl / (immerged_volume ** (1 / 3))) - 8) / 2.36)
        # print('c15=',c15)
        m1 = (0.0140407 * (self.Lwl / T_average)) - (1.75254 * (((immerged_volume) ** (1 / 3)) / self.Lwl)) - (
                    4.79323 * (self.B / self.Lwl)) - c16
        # print('m1=',m1)
        m2 = c15 * (self.Cp ** 2) * np.exp(-0.1 * (Fn ** (-2)))
        # print('m2=',m2)

        k1 = (c13 * (0.93 + (c12 * ((self.B / Lr) ** 0.92497)) * ((0.95 - self.Cp) ** (-0.521448)) * (
                    (1 - self.Cp + (0.0225 * (self.lcb / 100))) ** 0.6906))) - 1
        # print('k1=',k1)

        # calcul des différentes résistances
        Rf = 0.5 * Cf * WS * rho_eau * ((abs(V * 0.514)) ** 2)
        # print('Rf=', Rf)

        # additional pressure resistance
        Rtr = 0.5 * rho_eau * ((abs(V * 0.514)) ** 2) * self.At * c6
        # print('Rtr=', Rtr)

        # still-aire resistance
        if (self.Tf / self.Lwl) > 0.04:
            c4 = 0.04
        else:
            c4 = self.Tf / self.Lwl
        Ca = 0.006 * ((self.Lwl + 100) ** (-0.16)) - 0.00205 + (
                    0.003 * (np.sqrt(self.Lwl / 7.5)) * (Cb ** 4) * c2 * (0.04 - c4))
        ks = 0.000150
        Ca_add = (0.105 * (ks ** (1 / 3)) - 0.005579) / (self.Lwl ** (1 / 3))
        Ca_tot = Ca + Ca_add
        Ra = 0.5 * rho_eau * ((abs(V * 0.514)) ** 2) * WS * Ca_tot
        # print('Ra=',Ra)

        # bublbous bow resistance
        Pb = (0.56 * np.sqrt(self.Abt)) / (self.Tf - 1.5 * self.hb)
        if self.Abt == 0:
            Rb = 0
        else:
            Rb = (0.11 * np.exp(-3 * (Pb ** (-2))) * (Fni ** 3) * (self.Abt ** (1.5)) * rho_eau * g) / (1 + (Fni ** 2))
        # print('Rb=',Rb)

        # appendage resistance
        Sapp = self.S_rudder_behind_skeg + self.S_rudder_behind_stern + self.S_twin_screw_balance_rudders + self.S_shaft_brackets + self.S_skeg + self.S_strut_bossing + self.S_hull_bossings + self.S_shafts + self.S_stabilizer_fins + self.S_dome + self.S_bilge_keels
        k2 = ((
                          1.75 * self.S_rudder_behind_skeg + 1.4 * self.S_rudder_behind_stern + 2.8 * self.S_twin_screw_balance_rudders + 3.0 * self.S_shaft_brackets + 1.75 *
                          self.S_skeg + 3.0 * self.S_strut_bossing + 2.0 * self.S_hull_bossings + 3.0 * self.S_shafts + 2.8 * self.S_stabilizer_fins + 2.7 * self.S_dome + 1.4 * self.S_bilge_keels) / Sapp) - 1
        if Sapp == 0:
            Rapp = 0
        else:
            Rapp = 0.5 * rho_eau * ((abs(V * 0.514)) ** 2) * Sapp * (1 + k2) * Cf
        # print('Rapp=',Rapp)

        # resistance bow thruster
        Rbowt = rho_eau * ((abs(V * 0.514)) ** 2) * np.pi * (self.D ** 2) * 0.0075
        # print('Rbowt=',Rbowt)

        # wave resistance
        Rw = c1 * c2 * c5 * immerged_volume * rho_eau * g * np.exp(m1 * (Fn ** d) + m2 * np.cos(lambd * (Fn ** (-2))))
        # print('Rw=',Rw)

        return Rf * (1 + k1) + Rapp + Rw + Rb + Rtr + Ra + Rbowt

    def Stabilite(self, phi, theta):
        RMt = self.GMt * phi * self.displacement * g * 1000
        RMl = self.GMl * theta * self.displacement * g * 1000

        return RMt, RMl

    def Safran(self, V, deltasafran, lambd, phi):
        # formules hydro
        Veau = V * (np.sqrt((np.cos(lambd)) ** 2 + ((np.sin(lambd)) ** 2 * (np.cos(phi)) ** 2)))

        coord_saf = ([self.X_cos, self.Y_cos, self.Z_cos])
        coord_0_saf = ([self.X_0cos, self.Y_0cos, self.Z_0cos])

        # calcul des forces
        Lsaf = 0.5 * rho_eau * self.S_saf * (Veau ** 2) * self.Cl_saf
        Dsaf = 0.5 * rho_eau * self.S_saf * (Veau ** 2) * self.Cd_saf

        Fxsaf = -Dsaf
        Fysaf = Lsaf * np.cos(phi)
        Fzsaf = Lsaf * np.sin(phi)

        # changement de repère
        Msaf_bateau = (
        [[-np.cos(deltasafran), np.sin(deltasafran), 0], [-np.sin(deltasafran), -np.cos(deltasafran), 0], [0, 0, 1]])
        Mavance_bateau = ([[-np.cos(lambd), -np.cos(phi) * np.sin(lambd), np.sin(phi) * np.sin(lambd)],
                           [np.sin(lambd), np.cos(phi) * np.cos(lambd), -np.sin(phi) * np.cos(lambd)],
                           [0, np.sin(phi), np.cos(phi)]])
        coord_bateau = np.dot(Msaf_bateau, coord_saf) + coord_0_saf
        coord_avance_bateau = np.dot(Mavance_bateau, coord_bateau)
        # calcul des moments
        Mxsaf = coord_avance_bateau[1] * Fzsaf - coord_avance_bateau[2] * Fysaf
        Mysaf = coord_avance_bateau[2] * Fxsaf - coord_avance_bateau[0] * Fzsaf
        Mzsaf = coord_avance_bateau[0] * Fysaf - coord_avance_bateau[1] * Fxsaf

        return Fxsaf, Fysaf, Fzsaf, Mxsaf, Mysaf, Mzsaf

    def Derive(self, V, lambd, phi):
        # formules hydro
        Veau = V * (np.sqrt((np.cos(lambd)) ** 2 + ((np.sin(lambd)) ** 2 * (np.cos(phi)) ** 2)))

        coord_deriv = ([self.X_cod, self.Y_cod, self.Z_cod])
        coord_0_deriv = ([self.X_0cod, self.Y_0cod, self.Z_0cod])

        # calcul des forces
        Lderiv = 0.5 * rho_eau * self.S_deriv * (Veau ** 2) * self.Cl_deriv
        Dderiv = 0.5 * rho_eau * self.S_deriv * (Veau ** 2) * self.Cd_deriv

        Fxderiv = -Dderiv
        Fyderiv = Lderiv * np.cos(phi)
        Fzderiv = Lderiv * np.sin(phi)

        # changement de repère
        Mderiv_bateau = ([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
        Mavance_bateau = ([[-np.cos(lambd), -np.cos(phi) * np.sin(lambd), np.sin(phi) * np.sin(lambd)],
                           [np.sin(lambd), np.cos(phi) * np.cos(lambd), -np.sin(phi) * np.cos(lambd)],
                           [0, np.sin(phi), np.cos(phi)]])
        coord_bateau = np.dot(Mderiv_bateau, coord_deriv) + coord_0_deriv
        coord_avance_bateau = np.dot(Mavance_bateau, coord_bateau)
        # calcul des moments
        Mxderiv = coord_avance_bateau[1] * Fzderiv - coord_avance_bateau[2] * Fyderiv
        Myderiv = coord_avance_bateau[2] * Fxderiv - coord_avance_bateau[0] * Fzderiv
        Mzderiv = coord_avance_bateau[0] * Fyderiv - coord_avance_bateau[1] * Fxderiv

        return Fxderiv, Fyderiv, Fzderiv, Mxderiv, Myderiv, Mzderiv

    """
    propulsion vélique sera reprise dans chaque sous-classe de Bateau
    """

    @abstractmethod
    def Propulsion_velique(self):
        pass


class Aile_rigide(Bateau):
    def __init__(self, Lpp, Lwl, B, Tf, Ta, Abt, At, Cstern, Cp, Cm, Cwp, lcb, displacement, hb,
                 S_rudder_behind_skeg, S_rudder_behind_stern, S_twin_screw_balance_rudders, S_shaft_brackets, S_skeg,
                 S_strut_bossing,
                 S_hull_bossings, S_shafts, S_stabilizer_fins, S_dome, S_bilge_keels, D, X_cos, Y_cos, Z_cos, X_0cos,
                 Y_0cos, Z_0cos,
                 Cl_saf, Cd_saf, S_saf, X_cod, Y_cod, Z_cod, X_0cod, Y_0cod, Z_0cod, Cl_deriv, Cd_deriv, S_deriv, GMt,
                 GMl, S_voile, Cl_voile, Cd_voile, X_cov, Y_cov, Z_cov, X_0cov, Y_0cov, Z_0cov, Zref):
        super().__init__(Lpp, Lwl, B, Tf, Ta, Abt, At, Cstern, Cp, Cm, Cwp, lcb, displacement, hb,
                         S_rudder_behind_skeg, S_rudder_behind_stern, S_twin_screw_balance_rudders, S_shaft_brackets,
                         S_skeg, S_strut_bossing,
                         S_hull_bossings, S_shafts, S_stabilizer_fins, S_dome, S_bilge_keels, D, X_cos, Y_cos, Z_cos,
                         X_0cos, Y_0cos, Z_0cos,
                         Cl_saf, Cd_saf, S_saf, X_cod, Y_cod, Z_cod, X_0cod, Y_0cod, Z_0cod, Cl_deriv, Cd_deriv,
                         S_deriv, GMt, GMl)
        self.S_voile = S_voile
        self.Cl_voile = Cl_voile
        self.Cd_voile = Cd_voile
        self.X_cov = X_cov
        self.Y_cov = Y_cov
        self.Z_cov = Z_cov
        self.X_0cov = X_0cov
        self.Y_0cov = Y_0cov
        self.Z_0cov = Z_0cov
        self.Zref = Zref

    def Propulsion_velique(self, Vt, beta_t, V, lambd, phi):
        # formule aéro
        Vz = Vt * ((self.Z_cov / self.Zref) ** (1 / 7))  # prise en compte de l'altitude et de la répartition du vent
        Va = np.sqrt((Vz * np.sin(beta_t) * np.cos(phi)) ** 2 + (Vz * np.cos(beta_t) + V) ** 2)
        beta_phi = (np.pi / 2) - np.arctan(
            (Vz * np.cos(beta_t) + V) / (Vz * np.sin(beta_t) * np.cos(phi)))  # AWA avec prise en compte de la gîte

        delta_voile = (np.pi / 2) - np.arctan((Vz * np.cos(beta_t - lambd) + V) / (Vz * np.sin(beta_t - lambd) * np.cos(
            phi)))  # angle d'incidence de la voile + angle d'ouverture de celle-ci

        coord_voile = ([self.X_cov, self.Y_cov, self.Z_cov])
        coord_0_voile = ([self.X_0cov, self.Y_0cov, self.Z_0cov])

        Lvoile = 0.5 * rho_air * self.S_voile * (Va ** 2) * self.Cl_voile
        Dvoile = 0.5 * rho_air * self.S_voile * (Va ** 2) * self.Cd_voile
        Fxvoile = Lvoile * np.sin(beta_phi) - (Dvoile * np.cos(beta_phi))
        Fyvoile = -np.cos(phi) * ((Lvoile * np.sin(beta_phi)) + (Dvoile * np.cos(beta_phi)))
        Fzvoile = -np.sin(phi) * ((Lvoile * np.sin(beta_phi)) + (Dvoile * np.cos(beta_phi)))

        # changement de repère
        Mvoile_bateau = (
        [[-np.cos(delta_voile), np.sin(delta_voile), 0], [-np.sin(delta_voile), -np.cos(delta_voile), 0], [0, 0, 1]])
        Mavance_bateau = ([[-np.cos(lambd), -np.cos(phi) * np.sin(lambd), np.sin(phi) * np.sin(lambd)],
                           [np.sin(lambd), np.cos(phi) * np.cos(lambd), -np.sin(phi) * np.cos(lambd)],
                           [0, np.sin(phi), np.cos(phi)]])
        coord_bateau = np.dot(Mvoile_bateau, coord_voile) + coord_0_voile
        coord_avance_bateau = np.dot(Mavance_bateau, coord_bateau)

        # calcul des moments
        Mxvoile = coord_avance_bateau[1] * Fzvoile - coord_avance_bateau[2] * Fyvoile
        Myvoile = coord_avance_bateau[2] * Fxvoile - coord_avance_bateau[0] * Fzvoile
        Mzvoile = coord_avance_bateau[0] * Fyvoile - coord_avance_bateau[1] * Fxvoile

        return Fxvoile, Fyvoile, Fzvoile, Mxvoile, Myvoile, Mzvoile


def convergence(ListeV, Listelambda, Listephi, Listetheta, Listedeltasafran, convergence_V, convergence_lambda,
                convergence_phi, convergence_theta, convergence_deltasafran):
    if len(ListeV) < 3 or len(Listelambda) < 3 or len(Listephi) < 3 or len(Listetheta) < 3 or len(Listedeltasafran) < 3:
        return False
    ListeV = np.array(ListeV)
    Listelambda = np.array(Listelambda)
    Listephi = np.array(Listephi)
    Listetheta = np.array(Listetheta)
    Listedeltasafran = np.array(Listedeltasafran)
    ecart_V = ListeV[-5:].max() - ListeV[-5:].min()
    ecart_theta = Listetheta[-5:].max() - Listetheta[-5:].min()
    ecart_lambda = Listelambda[-5:].max() - Listelambda[-5:].min()
    ecart_phi = Listephi[-5:].max() - Listephi[-5:].min()
    ecart_deltasafran = Listedeltasafran[-5:].max() - Listedeltasafran[-5:].min()
    if ecart_V < convergence_V and ecart_lambda < convergence_lambda and ecart_phi < convergence_phi and ecart_deltasafran < convergence_deltasafran and ecart_theta < convergence_theta:
        return True
    return False


def jacobien(V, lambd, phi, theta, deltasafran, fx, fy, mx, my, mz):
    J = np.ones((5, 5))
    h = 1e-8

    # premiere ligne
    J[0, 0] = (fx(Fxvoile, Fxderiv, Fxsaf, Rtot) - fx(V, lambd, phi, theta, deltasafran)) / h
    J[0, 1] = (fx(Fxvoile, Fxderiv, Fxsaf, Rtot) - fx(V, lambd, phi, theta, deltasafran)) / h
    J[0, 2] = (fx(V, lambd, phi + h, theta, deltasafran) - fx(V, lambd, phi, theta, deltasafran)) / h
    J[0, 3] = (fx(V, lambd, phi, theta + h, deltasafran) - fx(V, lambd, phi, theta, deltasafran)) / h
    J[0, 4] = (fx(V, lambd, phi, theta, deltasafran + h) - fx(V, lambd, phi, theta, deltasafran)) / h

    # seconde ligne
    J[1, 0] = (fy(V + h, lambd, phi, theta, deltasafran) - fy(V, lambd, phi, theta, deltasafran)) / h
    J[1, 1] = (fy(V, lambd + h, phi, theta, deltasafran) - fy(V, lambd, phi, theta, deltasafran)) / h
    J[1, 2] = (fy(V, lambd, phi + h, theta, deltasafran) - fy(V, lambd, phi, theta, deltasafran)) / h
    J[1, 3] = (fy(V, lambd, phi, theta + h, deltasafran) - fy(V, lambd, phi, theta, deltasafran)) / h
    J[1, 4] = (fy(V, lambd, phi, theta, deltasafran + h) - fy(V, lambd, phi, theta, deltasafran)) / h

    # troisieme ligne
    J[2, 0] = (mx(V + h, lambd, phi, theta, deltasafran) - mx(V, lambd, phi, theta, deltasafran)) / h
    J[2, 1] = (mx(V, lambd + h, phi, theta, deltasafran) - mx(V, lambd, phi, theta, deltasafran)) / h
    J[2, 2] = (mx(V, lambd, phi + h, theta, deltasafran) - mx(V, lambd, phi, theta, deltasafran)) / h
    J[2, 3] = (mx(V, lambd, phi, theta + h, deltasafran) - mx(V, lambd, phi, theta, deltasafran)) / h
    J[2, 4] = (mx(V, lambd, phi, theta, deltasafran + h) - mx(V, lambd, phi, theta, deltasafran)) / h

    # quatrieme ligne
    J[3, 0] = (my(V + h, lambd, phi, theta, deltasafran) - my(V, lambd, phi, theta, deltasafran)) / h
    J[3, 1] = (my(V, lambd + h, phi, theta, deltasafran) - my(V, lambd, phi, theta, deltasafran)) / h
    J[3, 2] = (my(V, lambd, phi + h, theta, deltasafran) - my(V, lambd, phi, theta, deltasafran)) / h
    J[3, 3] = (my(V, lambd, phi, theta + h, deltasafran) - my(V, lambd, phi, theta, deltasafran)) / h
    J[3, 4] = (my(V, lambd, phi, theta, deltasafran + h) - my(V, lambd, phi, theta, deltasafran)) / h

    # cinquieme ligne
    J[4, 0] = (mz(V + h, lambd, phi, theta, deltasafran) - mz(V, lambd, phi, theta, deltasafran)) / h
    J[4, 1] = (mz(V, lambd + h, phi, theta, deltasafran) - mz(V, lambd, phi, theta, deltasafran)) / h
    J[4, 2] = (mz(V, lambd, phi + h, theta, deltasafran) - mz(V, lambd, phi, theta, deltasafran)) / h
    J[4, 3] = (mz(V, lambd, phi, theta + h, deltasafran) - mz(V, lambd, phi, theta, deltasafran)) / h
    J[4, 4] = (mz(V, lambd, phi, theta, deltasafran + h) - mz(V, lambd, phi, theta, deltasafran)) / h

    return J


def eq_X(Fxvoile, Fxderiv, Fxsaf, Rtot):
    Fxtot = Fxvoile + Fxderiv + Fxsaf - Rtot
    return Fxtot


def eq_Y(Fyvoile, Fyderiv, Fysaf):
    Fytot = Fyvoile + Fyderiv + Fysaf
    return Fytot


def eq_mx(Mxvoile, Mxderiv, Mxsaf, RMt):
    Mxtot = Mxvoile + Mxderiv + Mxsaf + RMt
    return Mxtot


def eq_my(Myvoile, Myderiv, Mysaf, RMl):
    Mytot = Myvoile + Myderiv + Mysaf + RMl
    return Mytot


def eq_mz(Mzvoile, Mzderiv, Mzsaf):
    Mztot = Mzvoile + Mzderiv + Mzsaf
    return Mztot



def VPP(Vt, beta_t):
    # hypotheses de départ
    V0, lambd0, phi0, theta0, deltasafran0 = 6.17, 0.1, 0.1, 0.1, 0.1
    Bateau = Aile_rigide(Lpp=170, Lwl=180, B=31, Tf=9, Ta=9, Abt=0, At=0, Cstern=-25, Cp=0.583, Cm=0.985, Cwp=0.837,
                         lcb=-4, displacement=35800, hb=0,
                         S_rudder_behind_skeg=0, S_rudder_behind_stern=0, S_twin_screw_balance_rudders=0,
                         S_shaft_brackets=0, S_skeg=100, S_strut_bossing=0,
                         S_hull_bossings=0, S_shafts=0, S_stabilizer_fins=0, S_dome=0, S_bilge_keels=0, D=0,
                         X_cos=-89.0, Y_cos=0, Z_cos=-6.5, X_0cos=-89.0, Y_0cos=0, Z_0cos=0,
                         Cl_saf=0.45, Cd_saf=0.0025, S_saf=40, X_cod=0, Y_cod=0, Z_cod=0, X_0cod=0, Y_0cod=0, Z_0cod=0,
                         Cl_deriv=0, Cd_deriv=0, S_deriv=0, GMt=1.318, GMl=0, S_voile=2048,
                         Cl_voile=2.0, Cd_voile=0.3, X_cov=-6, Y_cov=0, Z_cov=39.5, X_0cov=-6, Y_0cov=0, Z_0cov=0,
                         Zref=10)

    iter = 0
    Listeiter = [iter]
    ListeV = [V0]
    Listelambda = [lambd0]
    Listephi = [phi0]
    Listetheta = [theta0]
    Listedeltasafran = [deltasafran0]

    # critère de convergence
    X = np.array([V0, lambd0, phi0, theta0, deltasafran0])
    condition_convergence = [0.01, 0.1 * np.pi / 180, 0.1 * np.pi / 180, 0.1 * np.pi / 180,
                             0.1 * np.pi / 180]  # Critère de convergence
    print("Le calcul a bien démarré")

    while iter < 50 and not convergence(ListeV, Listelambda, Listephi, Listetheta, Listedeltasafran,
                                        condition_convergence[0], condition_convergence[1], condition_convergence[2],
                                        condition_convergence[3],
                                        condition_convergence[4]):  # regarder l'écart entre les 5 dernières valeurs?
        iter += 1

        V = X[0]
        lambd = X[1]
        phi = X[2]
        theta = X[3]
        deltasafran = X[4]

        if iter >= 5 and lambd > 10 * np.pi / 180:
            raise ValueError("Le bateau dérive trop")

        if iter >= 5 and phi > 30 * np.pi / 180:
            raise ValueError("La gite est trop importance")

        if iter >= 5 and theta > 10 * np.pi / 180:
            raise ValueError("Le bateau pique trop")

        if iter >= 5 and deltasafran > 20 * np.pi / 180:
            raise ValueError("L'angle de safran est trop élevé")

        Fxsaf, Fysaf, Fzsaf, Mxsaf, Mysaf, Mzsaf = Bateau.Safran(V, deltasafran, lambd, phi)
        Fxderiv, Fyderiv, Fzderiv, Mxderiv, Myderiv, Mzderiv = Bateau.Derive(V, lambd, phi)
        Rtot = Bateau.Resistance_avancement(V)
        Fxvoile, Fyvoile, Fzvoile, Mxvoile, Myvoile, Mzvoile = Bateau.Propulsion_velique(Vt, beta_t, V, lambd, phi)
        RMt, RMl = Bateau.Stabilite(phi, theta)



        # Construction de la Jacobienne:
        J = jacobien(V, lambd, phi, theta, deltasafran, eq_X, eq_Y, eq_mx, eq_my, eq_mz)
        print('J = ', J)
        M = np.array([eq_Y(Fyvoile, Fyderiv, Fysaf), eq_Y(Fyvoile, Fyderiv, Fysaf),
                      eq_mx(Mxvoile, Mxderiv, Mxsaf, RMt), eq_my(Myvoile, Myderiv, Mysaf, RMl),
                      eq_mz(Mzvoile, Mzderiv, Mzsaf)])
        print('M =', M)
        # Rebouclage
        X = X - np.linalg.inv(J) @ M

        # Garder les valeurs pour effectuer un tracé graphique
        Listeiter.append(iter)
        ListeV.append(X[0])
        Listelambda.append(X[1])
        Listephi.append(X[2])
        Listetheta.append(X[3])
        Listedeltasafran.append(X[4])

        P_voile = Fxvoile * X[0]
    return X, P_voile, Listeiter, ListeV, Listelambda, Listephi, Listetheta, Listedeltasafran


if __name__ == "__main__":
    rho_air, rho_eau = 1.292, 1.030
    g = 9.80
    nu = 0.000001140

    X, Listeiter, ListeV, Listelambda, Listephi, Listetheta, Listedeltasafran = VPP(10, 0.15)
