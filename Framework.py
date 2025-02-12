import numpy as np  # On importe la bibliothèque numpy
import numpy.random as rd  # On importe le module random de numpy qui va nous aider dans la génération de nombres aléatoires
import matplotlib  # On importe la bibliothèque matplotlib
import matplotlib.pyplot as plt  # On importe le module pyplot de matplotlib pour créer des graphiques
import warnings  # On importe le module warnings pour gérer les avertissements
from tabulate import tabulate  # On importe la fonction tabulate pour afficher les résultats sous forme de magnifiques tableaux

warnings.simplefilter(action="ignore", category=FutureWarning)  # On ingore les avertissements de la catégorie
# FutureWarning


class Player:  # On crée une classe Player pour représenter un joueur du dilemme du prisonnier
    def __init__(self, strategy, starting_balance=0, name=None, prob=0.5):  # Initialisation : on initialise un
        # joueur avec une stratégie, un solde de départ, un nom et une probabilité
        self.strategy = strategy  # Attribution de la stratégie au joueur
        self.decision = []  # Création d'une liste vide pour stocker les décisions du joueur
        self.balance = starting_balance  # Attribution du solde de départ au joueur
        self.name = name  # Attribuer du nom au joueur
        self.prob = prob  # Attribution de la probabilité au joueur

    def cooperate(self):  # Définition de la méthode de coopération
        self.decision.append("C")  # Ajouter "C" à la liste des décisions pour indiquer la coopération

    def defect(self):  # Définition de la méthode de trahison
        self.decision.append("D")  # Ajouter "D" à la liste des décisions pour indiquer la trahison


class Game:


# Initialise la classe avec les arguments fournis
    def __init__(self, n, player1, player2, payoff_matrix=[4, 3, 1, 0]):
        self.n = n  # Nombre de tours à jouer
        self.Player1 = player1  # Premier joueur
        self.Player2 = player2  # Deuxième joueur
        self.CC = 0  # Nombre de coopérations mutuelles (C|C)
        self.CD = 0  # Nombre de coopérations du joueur 1 et défections du joueur 2 (C|D)
        self.DC = 0  # Nombre de défections du joueur 1 et coopérations du joueur 2 (D|C)
        self.DD = 0  # Nombre de défections mutuelles (D|D)
        self.balance_tracking = np.zeros((2, self.n))  # Suivi des soldes des deux joueurs pour chaque tour
        self.interaction_tracking = np.zeros((4, self.n))  # Suivi des interactions pour chaque tour
        self.temptation = payoff_matrix[0]  # Gain pour la tentation (T)
        self.reward = payoff_matrix[1]  # Gain pour la récompense (R)
        self.punishment = payoff_matrix[2]  # Gain pour la punition (P)
        self.sucker = payoff_matrix[3]  # Gain pour le pigeon (S)
        self.prob1 = player1.prob  # Probabilité de coopération du joueur 1
        self.prob2 = player2.prob  # Probabilité de coopération du joueur 2


# Méthode pour exécuter la partie
    def run(self, show="cnsl", save=False):
        # Initialise les variables pour stocker les stratégies et les états des joueurs
        strats = [self.Player1.strategy, self.Player2.strategy]
        players = [self.Player1, self.Player2]
        pavlov = [False, False]  # Variable pour stocker si le joueur utilise la stratégie Pavlov
        interaction_labels = ["C|C", "C|D", "D|C", "D|D"]  # Labels pour les interactions
        probs = [self.prob1, self.prob2]  # Probabilités de coopération pour les deux joueurs

        # Boucle sur les tours de jeu
        for i in range(self.n):

            # Boucle sur les joueurs
            for j in range(2):

                # Vérifie si la stratégie du joueur est Pavlov et met à jour la stratégie si nécessaire
                if (strats[j] == "pavlov") or (pavlov[j]):
                    pavlov[j] = True  # Rendre la variable pavlov[j] vraie
                    # Si le tour actuel est divisible par 6
                    if i % 6 == 0:

                        if len(players[j].decision) < 6:  # Si la longueur des décisions du joueur est inférieure à 6
                            strats[j] = "tit_for_tat"  # Changer la stratégie du joueur à "tit_for_tat"

                        elif players[1 - j].decision[-6:].count(
                                "D") > 4:  # Si l'adversaire a trahi plus de 4 fois sur les 6 derniers tours
                            strats[j] = "def_all"  # Changer la stratégie du joueur à "def_all"

                        elif players[1 - j].decision[-6:].count(
                                "D") == 4:  # Si l'adversaire a trahi exactement 4 fois sur les 6 derniers tours
                            strats[j] = "tit_for_two_tats"  # Changer la stratégie du joueur à "tit_for_two_tats"

                        elif players[1 - j].decision[-6:].count(
                                "D") == 0:  # Si l'adversaire n'a pas trahi sur les 6 derniers tours
                            strats[j] = "tit_for_tat"
                        # Pour tous les autres cas
                        else:
                            strats[j] = "def_all"  # Changer la stratégie du joueur à "def_all"

                # Si la stratégie du joueur est "prober"
                if strats[j] == "prober":
                    # Si le joueur n'a pas encore pris de décision
                    if len(players[j].decision) == 0:
                        players[j].defect()  # Le joueur trahit

                    elif len(players[j].decision) <= 2:  # Si le joueur a pris 1 ou 2 décisions
                        players[j].cooperate()  # le joueur coopère
                    # Pour les autres cas
                    else:
                        if players[1 - j].decision[1:3] == ["C", "C"]:   # Si les deux premières décisions de
                                                                            # l'adversaire sont coopération
                            players[j].defect()  # Le joueur trahit
                        # sinon
                        else:
                            strats[j] = "tit_for_tat"  # Changer la stratégie du joueur à "tit_for_tat"

                # Si la stratégie du joueur est "coop_all"
                if strats[j] == "coop_all":
                    players[j].cooperate()  # Le joueur coopère

                # Si la stratégie du joueur est "def_all"
                elif strats[j] == "def_all":
                    players[j].defect()  # Le joueur trahit

                # Si la stratégie du joueur est "tit_for_tat"
                elif strats[j] == "tit_for_tat":

                    if len(players[j].decision) == 0 or len(
                            players[1 - j].decision) == 0:  # Si le joueur ou l'adversaire n'a pas encore pris de décision
                        players[j].cooperate()  # le joueur coopère
                    # Sinon (le joueur et l'adversaire ont déjà pris des décisions)
                    else:
                        players[j].decision.append(players[1 - j].decision[
                                                       -1])  # Le joueur prend la même décision que l'adversaire au tour précédent

                # Si la stratégie du joueur est "tit_for_two_tats"
                elif strats[j] == "tit_for_two_tats":

                    if (len(players[1 - j].decision) > 2):  # Si l'adversaire a pris plus de 2 décisions

                        if (players[1 - j].decision[-1] == "D") & (
                                players[1 - j].decision[-2] == "D"):  # Si l'adversaire a trahi lors des deux derniers tours
                            players[j].defect()  # Le joueur trahit
                        # sinon
                        else:
                            players[j].cooperate()  # Le joueur coopère
                    # Si l'adversaire a pris 2 décisions ou moins
                    else:
                        players[j].cooperate()  # Le joueur coopère

                # Si la stratégie du joueur est "two_tits_for_tat"
                elif strats[j] == "two_tits_for_tat":

                    if len(players[1 - j].decision) <= 1:  # Si l'adversaire a pris 1 décision ou moins
                        players[j].cooperate()  # Le joueur coopère

                    elif (players[1 - j].decision[-1] == "D") or (players[1 - j].decision[
                                                                      -2] == "D"):  # Si l'adversaire a trahi lors d'un des deux derniers tours
                        players[j].defect()  # Le joueur trahit
                    # Sinon
                    else:
                        players[j].cooperate()  # Le joueur coopère

                # Si la stratégie du joueur est "random"
                elif strats[j] == "random":
                    test_variable = rd.rand(1)  # Génère un nombre aléatoire entre 0 et 1

                    if test_variable > probs[j]:  # Si le nombre aléatoire est supérieur à la probabilité du joueur
                        players[j].cooperate()  # Le joueur coopère
                    # Sinon
                    else:
                        players[j].defect()  # Le joueur trahit

                # Si la stratégie du joueur est "grim_trigger"
                elif strats[j] == "grim_trigger":

                    if np.any(np.array(players[1 - j].decision) == "D"):  # Si l'adversaire a déjà trahi
                        players[j].defect()  # Le joueur trahit
                    # Sinon
                    else:
                        players[j].cooperate()  # Le joueur coopère

                # Si la stratégie du joueur est "gradual_oneupper"
                elif strats[j] == "gradual_oneupper":

                    if players[1 - j].decision.count("D") * 3 <= 2 * players[j].decision.count(
                            "D"):  # Si le joueur a trahi moins de deux fois plus que l'adversaire
                        players[j].cooperate()  # Le joueur coopère
                    # Sinon
                    else:
                        players[j].defect()  # Le joueur trahit

                # Si la stratégie du joueur est "majority"
                elif strats[j] == "majority":

                    if players[1 - j].decision.count("C") >= players[1 - j].decision.count(
                            "D"):  # Si l'adversaire a coopéré plus souvent qu'il a trahi
                        players[j].cooperate()  # Le joueur coopère
                    # Sinon
                    else:
                        players[j].defect()  # Le joueur trahit

                # Si la stratégie du joueur est "handshake"
                elif strats[j] == "handshake":

                    if len(players[j].decision) == 0:  # Si c'est le premier tour
                        players[j].defect()  # Le joueur trahit

                    elif len(players[j].decision) == 1:  # Si c'est le deuxième tour
                        players[j].cooperate()  # Le joueur coopère
                    # Pour les tours suivants
                    else:

                        if players[1 - j].decision[:2] == ["D",
                                                           "C"]:  # Si l'adversaire a trahi puis coopéré lors des deux premiers tours
                            players[j].cooperate()  # Le joueur coopère
                        # Sinon
                        else:
                            players[j].defect()  # Le joueur trahit

                # Si la stratégie du joueur est "naive_prober"
                elif strats[j] == "naive_prober":

                    if len(players[j].decision) == 0 or len(players[
                                                                1 - j].decision) == 0:  # Si c'est le premier tour ou si l'adversaire n'a pas encore pris de décision
                        players[j].cooperate()  # Le joueur coopère

                    elif rd.random() < 0.1:  # Si le nombre aléatoire est inférieur à 0,1
                        players[j].defect()  # Le joueur trahit
                    # Sinon
                    else:
                        players[j].decision.append(
                            players[1 - j].decision[-1])  # Le joueur prend la dernière décision de l'adversaire

                # Si la stratégie du joueur est "remorseful_prober"
                elif strats[j] == "remorseful_prober":

                    if len(players[j].decision) == 0 or len(players[
                                                                1 - j].decision) == 0:  # Si c'est le premier tour ou si l'adversaire n'a pas encore pris de décision
                        players[j].cooperate()  # Le joueur coopère

                    elif len(players[j].decision) > 1 and players[j].decision[-1] == "D" and players[1 - j].decision[
                        -1] == "D":  # Si le joueur a trahi lors du tour précédent et l'adversaire aussi
                        players[j].cooperate()  # Le joueur coopère

                    elif rd.random() < 0.1:  # Si le nombre aléatoire est inférieur à 0,1
                        players[j].defect()  # Le joueur trahit
                    # Sinon
                    else:
                        players[j].decision.append(
                            players[1 - j].decision[-1])  # Le joueur prend la dernière décision de l'adversaire


                else:
                    players[j].decision.append("Invalid strategy")
                    # Si aucune stratégie correspondante n'est trouvée, ajoute "Invalid strategy" à la décision du joueur.

            last_decision_1 = players[0].decision[-1]
            last_decision_2 = players[1].decision[-1]
            # Récupère les dernières décisions des deux joueurs.

            if last_decision_1 == last_decision_2: # Si les deux joueurs ont pris la même décision :

                if last_decision_1 == "C":
                    players[0].balance += self.reward
                    players[1].balance += self.reward
                    self.CC += 1  # Si les deux joueurs ont coopéré, mise à jour de leurs soldes et incrémente le
                                    # compteur de coopérations mutuelles.

                elif last_decision_1 == "D":
                    players[0].balance += self.punishment
                    players[1].balance += self.punishment
                    self.DD += 1 # Si les deux joueurs ont trahi, mise à jour de leurs soldes et incrémente le
                                    # compteur de trahisons mutuelles.

            if last_decision_1 != last_decision_2: # Si les deux joueurs ont pris des décisions différentes :

                if last_decision_1 == "C":
                    players[0].balance += self.sucker
                    players[1].balance += self.temptation
                    self.CD += 1 # Si le joueur 1 coopère et le joueur 2 trahit, mise à jour de leurs soldes et
                                    # incrémente le compteur de coopération/trahison.

                elif last_decision_1 == "D":
                    players[0].balance += self.temptation
                    players[1].balance += self.sucker
                    self.DC += 1
                    # Si le joueur 1 trahit et le joueur 2 coopère, mise à jour de leurs soldes et incrémente le compteur de trahison/coopération.

            # Met à jour le suivi des soldes et des interactions pour chaque joueur et chaque tour
            self.balance_tracking[0, i] = players[0].balance
            self.balance_tracking[1, i] = players[1].balance
            self.interaction_tracking[0, i] = self.CC
            self.interaction_tracking[1, i] = self.CD
            self.interaction_tracking[2, i] = self.DC
            self.interaction_tracking[3, i] = self.DD
        # Si l'affichage est demandé sur la console ou sur tous les supports
        if show == "cnsl" or show == "all":
            # Si le nom d'un joueur n'est pas défini, lui attribuer un nom par défaut
            for i in range(2):
                if players[i].name == None:
                    players[i].name == f"Player {i + 1}"

            # Préparation de la matrice de gains pour l'affichage
            payoff_matrix_print = [[f"({self.reward}, {self.reward})", f"({self.sucker}, {self.temptation})"],
                                   [f"({self.temptation}, {self.sucker})", f"({self.punishment}, {self.punishment})"]]
            headers = ["Cooperate", "Defect"]  # Strategies
            rows = ["Cooperate", "Defect"]  # Strategies
            print("Using payoff matrix:")
            print(tabulate(payoff_matrix_print, headers=headers, showindex=rows, tablefmt="grid"))
            print(f"{players[0].name} ({players[0].strategy} strategy) chose: {players[0].decision}")
            print(f"{players[1].name} ({players[1].strategy} strategy) chose: {players[1].decision}")
            print(f"C|C: {self.CC}, C|D: {self.CD}, D|C: {self.DC}, D|D: {self.DD}.")
            print(f"{players[0].name} ({players[0].strategy} strategy) final balance: {players[0].balance}")
            print(f"{players[1].name} ({players[1].strategy} strategy) final balance: {players[1].balance}")
        # Si show est "fig" ou "all", affiche des graphiques des résultats
        if show == "fig" or show == "all":
            plt.style.use("dark_background")
            # Crée une figure avec plusieurs sous-graphiques
            fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(16, 16),
                                    gridspec_kw={'width_ratios': [3, 4]})
            # Diagramme à barres des soldes finaux des deux joueurs
            axs[0, 0].bar([0.5, 1], [players[0].balance, players[1].balance],
                          width=0.5, edgecolor="white", color=["#b255fa", "#55fa8f"])
            axs[0, 0].set_title(f"Payoff")
            axs[0, 0].set_ylabel("Payoff")
            axs[0, 0].set_xticks([0.5, 1])
            axs[0, 0].set_xticklabels([f"{players[0].name}, {players[0].strategy}", f"{players[1].name}, {players[1].strategy}"])
            axs[0, 0].set_xlim((0, 1.5))
            # Évolution des soldes des deux joueurs au fil des tours
            axs[0, 1].set_title("Payoff evolution")
            axs[0, 1].plot(np.arange(1, self.n + 1), self.balance_tracking[0], label=f"{players[0].name},{players[0].strategy}",
                           color="#b255fa")
            axs[0, 1].plot(np.arange(1, self.n + 1), self.balance_tracking[1], label=f"{players[1].name},{players[1].strategy}",
                           color="#55fa8f")
            axs[0, 1].set_ylabel("Total player payoff")
            axs[0, 1].set_xlabel("Turn number")
            axs[0, 1].legend()
            axs[0, 1].grid(color="gray", linewidth=0.7)
            # Diagramme à barres du nombre d'interactions de chaque type
            colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
            axs[1, 0].bar([0.5, 1, 1.5, 2], [self.CC, self.CD, self.DC, self.DD],
                          width=0.5, edgecolor="white", color=colours)
            axs[1, 0].set_title(f"Interactions")
            axs[1, 0].set_ylabel("Number of interactions")
            axs[1, 0].set_xlabel(f"Types of interactions ({players[0].name},{players[0].strategy} | {players[1].name},{players[1].strategy})")
            axs[1, 0].set_xticks([0.5, 1, 1.5, 2])
            axs[1, 0].set_xticklabels(interaction_labels)
            axs[1, 0].set_xlim((0, 2.5))
            # Évolution du nombre total d'interactions de chaque type après chaque tour
            for i in range(4):
                axs[1, 1].plot(np.arange(1, self.n + 1), self.interaction_tracking[i], label=interaction_labels[i])
            axs[1, 1].set_title("Total interactions after each round")
            axs[1, 1].set_ylabel("Number of interactions")
            axs[1, 1].set_xlabel("Turn number")
            axs[1, 1].grid(color="gray", linewidth=0.7)
            axs[1, 1].legend()
            # Graphique de la différence de solde relative entre les deux joueurs après chaque tour
            ax5 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
            ax5.plot(np.arange(1, self.n + 1), (self.balance_tracking[0] - self.balance_tracking[1]))
            ax5.set_title(f"Relative payoff ({players[0].name},{players[0].strategy} - {players[1].name}"
                          f",{players[1].strategy})")
            ax5.set_ylabel("Relative payoff")
            ax5.set_xlabel("Turn number")

            plt.suptitle(
                f"Prisoner's dilemma results: {players[0].name} ({players[0].strategy}) vs {players[1].name} ({players[1].strategy}) ({self.n} rounds)")

            plt.tight_layout()

            if save:
                plt.savefig(f"IPD__{players[0].strategy}__vs__{players[1].strategy}.jpg")

            plt.show()

        # Return les résultats sous forme de listes
        return [players[0].balance, players[1].balance, self.CC, self.CD, self.DC, self.DD], [self.balance_tracking,
                                                                                              self.interaction_tracking]
