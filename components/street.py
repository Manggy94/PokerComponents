import numpy as np
import components.constants as cst


class Street:
    """Class initiating a Street with its players and actions"""

    def __init__(self, name="PF"):
        self.name = f"{cst.Street(name)}"
        self.cards = []
        self.active_players = []
        self.actions = []
        self.street_pot = 0
        self.highest_bet = 0
        self.index = 0
        self.it = None
        self.init_pl = None
        self.current_pl = None

    def get_action(self, i):
        try:
            return self.actions[i]
        except IndexError:
            return None

    def get_action_info(self, i):
        try:
            action = self.actions[i]
            return action.player.seat, action.move, action.value
        except IndexError:
            return None, None, None

    def get_actions_infos(self, n: int = 24):
        return np.hstack([self.get_action_info(i) for i in range(n)])

    @property
    def remaining_players(self):
        return [pl for pl in self.active_players if not pl.folded]

    @property
    def not_all_in_players(self):
        return [pl for pl in self.remaining_players if not pl.is_all_in]

    def reset_bets(self):
        self.highest_bet = 0
        for player in self.active_players:
            player.current_bet = 0

    def update_table(self):
        for i in range(len(self.active_players)):
            pl = self.active_players[i]
            if pl.folded:
                print(f"{pl.name} folded and is off this hand")
                self.active_players.remove(pl)

    def next_player(self):
        try:
            pl = next(self.it)
            return pl
        except StopIteration:
            self.it = iter(self.remaining_players)
            return next(self.it)
        except TypeError:
            self.it = iter(self.remaining_players)
            return next(self.it)
