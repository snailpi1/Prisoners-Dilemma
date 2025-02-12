import tkinter as tk
from Framework import Game, Player
from tabulate import tabulate

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Game")

        self.strategy1_label = tk.Label(master, text="Player 1 strategy:")
        self.strategy1_label.pack()
        self.strategy1_entry = tk.Entry(master)
        self.strategy1_entry.pack()

        self.strategy2_label = tk.Label(master, text="Player 2 strategy:")
        self.strategy2_label.pack()
        self.strategy2_entry = tk.Entry(master)
        self.strategy2_entry.pack()

        self.payoff_label = tk.Label(master, text="Payoff matrix:")
        self.payoff_label.pack()
        self.payoff_entry = tk.Entry(master)
        self.payoff_entry.pack()

        self.rounds_label = tk.Label(master, text="Number of rounds:")
        self.rounds_label.pack()
        self.rounds_entry = tk.Entry(master)
        self.rounds_entry.pack()

        self.run_button = tk.Button(master, text="Run", command=self.run)
        self.run_button.pack()

        self.result_text = tk.Text(master)
        self.result_text.pack()

    def run(self):
        strategy1 = self.strategy1_entry.get()
        strategy2 = self.strategy2_entry.get()
        payoff = self.payoff_entry.get()
        rounds = int(self.rounds_entry.get())

        gamedef = Game(rounds, Player(strategy1), Player(strategy2), payoff_matrix=payoff)
        results, tracking = gamedef.run()

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Results:\n")
        self.result_text.insert(tk.END, "Player 1 balance: {}\n".format(results[0]))
        self.result_text.insert(tk.END, "Player 2 balance: {}\n".format(results[1]))
        self.result_text.insert(tk.END, "CC: {}\n".format(results[2]))
        self.result_text.insert(tk.END, "CD: {}\n".format(results[3]))
        self.result_text.insert(tk.END, "DC: {}\n".format(results[4]))
        self.result_text.insert(tk.END, "DD: {}\n".format(results[5]))

root = tk.Tk()
