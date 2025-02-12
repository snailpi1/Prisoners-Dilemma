from Framework import Game, Player

strategies = ["coop_all", "def_all", "random", "tit_for_tat", "two_tits_for_tat", "tit_for_two_tats", "prober", "grim_trigger", "gradual_oneupper", "majority", "handshake", "naive_prober", "remorseful_prober", "pavlov"]
show = "cnsl"
show = "fig"  # À DECOMMENTER POUR VOIR TOUS LES GRAPHIQUES


Alice = Player(strategies[7], name= "Alice")
Bob = Player("random", name= "Bob")

game = Game(30, Alice, Bob)
game.run(show="fig", save=True)
