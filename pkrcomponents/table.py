from pkrcomponents.board import Board
from pkrcomponents.card import Deck
from pkrcomponents.constants import Street
from pkrcomponents.players import Players
from pkrcomponents.pot import Pot
from pkrcomponents.tournament import Level, Tournament
from pkrcomponents.evaluator import Evaluator


class Table:
    """Class representing a poker table"""
    _ident: str
    _board: Board
    _deck: Deck
    _players: Players
    _pots: [Pot]
    _max_players: int
    _is_mtt: bool
    _tournament: Tournament
    _level: Level
    _street: Street
    _seat_playing: int
    _min_bet: float
    _evaluator: Evaluator

    def __init__(self, max_players=6):
        self._board = Board()
        self._deck = Deck()
        self._deck.shuffle()
        self._players = Players()
        self._pot = Pot()
        self._evaluator = Evaluator()
        self._is_mtt = False
        self._street = Street.PREFLOP
        self.max_players = max_players

    @property
    def board(self):
        """Returns the associated board """
        return self._board

    @property
    def deck(self):
        """Returns the associated deck """
        return self._deck

    @property
    def players(self):
        """Returns the associated players """
        return self._players

    @property
    def max_players(self):
        """Returns the maximum players that can be added on this table"""
        return self._max_players

    @max_players.setter
    def max_players(self, max_value):
        """Setter for max players property"""
        if max_value not in range(1, 11):
            raise ValueError("Number of players should be between 1 and 10")
        else:
            self._max_players = max_value

    @property
    def pot(self):
        """Returns the associated pot """
        return self._pot

    @property
    def tournament(self):
        """Returns the associated tournament """
        return self._tournament

    @property
    def evaluator(self):
        """Returns the associated evaluator"""
        return self._evaluator

    @tournament.setter
    def tournament(self, tournament):
        """Setter for tournament property"""
        self._tournament = tournament

    @property
    def street(self):
        """Returns table's current street"""
        return self._street

    @street.setter
    def street(self, street):
        """Setter for street property"""
        self._street = Street(street)

    @property
    def level(self):
        """Returns current level"""
        if self._is_mtt:
            return self._tournament.level
        else:
            return self._level

    @level.setter
    def level(self, level):
        """Setter for level property"""
        self._level = level

    @property
    def playing_order(self):
        """Returns the list of the indexes of players on the table, with order depending on current street"""
        if self._street == Street.PREFLOP:
            return self.players.preflop_ordered_seats
        else:
            return self.players.postflop_ordered_seats

    @property
    def players_waiting(self):
        """Returns the list of players on the table that are waiting to play"""
        return [self.players[i] for i in self.playing_order if self.players[i].can_play]

    @property
    def players_in_game(self):
        """Returns the list of players on the table that are still in the game (they can make an action)"""
        return [self.players[i] for i in self.playing_order if self.players[i].in_game]

    @property
    def players_involved(self):
        """Returns the list of players on the table that didn't fold yet"""
        return [self.players[i] for i in self.playing_order if not self.players[i].folded]

    @property
    def seats_playing(self):
        """Returns the list of seats of players waiting to play"""
        return [pl.seat for pl in self.players_waiting]

    @property
    def nb_waiting(self):
        """Returns the number of players waiting to play"""
        return len(self.players_waiting)

    @property
    def nb_involved(self):
        """Returns the number of players who didn't fold yet"""
        return len(self.players_involved)

    def draw_flop(self, c1=None, c2=None, c3=None):
        """For the flop, draws 3 cards in the deck and adds them on the board as flop cards"""
        if len(self._board) > 0:
            raise ValueError("Board must be empty before we can draw a flop")
        c1 = self._deck.draw(c1)
        c2 = self._deck.draw(c2)
        c3 = self._deck.draw(c3)
        self._board.add(c1)
        self._board.add(c2)
        self._board.add(c3)

    def flop(self, c1=None, c2=None, c3=None):
        """Draw a flop and steps to this new street"""
        self.draw_flop(c1=c1, c2=c2, c3=c3)
        self.street = "flop"
        self.street_reset()

    def draw_turn(self, card=None):
        """For the turn, draws a card in the deck and adds it on the board as turn card"""
        if len(self._board) != 3:
            raise ValueError("Board size must be 3 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def turn(self, card=None):
        """Draw a turn and steps to this new street"""
        self.draw_turn(card)
        self.street = "turn"
        self.street_reset()

    def draw_river(self, card=None):
        """For the river, draws a card in the deck and adds it on the board as river card"""
        if len(self._board) != 4:
            raise ValueError("Board size must be 4 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def river(self, card=None):
        """Draw a river and steps to this new street"""
        self.draw_river(card)
        self.street = "river"
        self.street_reset()

    def add_tournament(self, tournament):
        """Associates table with a tournament"""
        self.tournament = tournament
        self._is_mtt = True

    def post_antes(self):
        """Preflop Ante posting for players on the table"""
        for i in self.players.preflop_ordered_seats:
            player = self.players.seat_dict[i]
            player.post(self.level.ante)

    def post_sb(self):
        """Preflop small blind posting"""
        seat = self.players.seats_mapper["SB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.sb)
            player.played = False

    def post_bb(self):
        """Preflop big blind posting"""
        seat = self.players.seats_mapper["BB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.bb)
            player.played = False

    def post_pregame(self):
        """Preflop posting antes and blinds"""
        self.post_antes()
        self.post_sb()
        self.post_bb()

    @property
    def seat_playing(self):
        """Returns the seat of the player currently playing"""
        if not hasattr(self, "_seat_playing"):
            self._seat_playing = self.playing_order[0]
        return self._seat_playing

    @property
    def min_bet(self):
        """Returns table current minimum bet a player can make"""
        if not hasattr(self, "_min_bet"):
            self._min_bet = self.level.bb*2
        return self._min_bet

    @min_bet.setter
    def min_bet(self, value):
        """Setter for min bet property"""
        if value > self.min_bet:
            self._min_bet = value

    def advance_seat_playing(self):
        """Advances seat playing to next available player"""
        player = self.current_player
        while not player.can_play and self.nb_waiting > 0:
            idx = self.playing_order.index(player.seat) + 1
            try:
                new_seat = self.playing_order[idx]
            except IndexError:
                new_seat = self.playing_order[0]
            player = self.players[new_seat]
        self._seat_playing = player.seat

    def street_reset(self):
        """Reset status of players in game and betting status for a new street"""
        self.pot.highest_bet = 0
        self.min_bet = self.level.bb
        for player in self.players_in_game:
            player.reset_street_status()

    @property
    def current_player(self):
        """Returns the player currently playing"""
        return self.players[self.seat_playing]

    @property
    def winners(self):
        """Current status of winners with associated scores"""
        winners = {}
        for player in self.players_involved:
            pl_score = player.hand_score
            if not winners.get(pl_score):
                winners[pl_score] = [player]
            else:
                winners[pl_score].append(player)
        return winners

    def split_pot(self, players):
        """Split pot between players"""
        while len(players) > 0 and self.pot.value > 0:
            min_reward = min([pl.max_reward for pl in players])
            reward = min(min_reward, self.pot.value/len(players))
            for player in players:
                if not hasattr(player, "reward"):
                    player.reward = 0
                player.reward += reward
                if player.reward >= player.max_reward:
                    players.remove(player)
                    player.win(reward)

    def distribute_rewards(self):
        """Distribute rewards between players"""
        scores = [score for score in self.winners.keys()]
        scores.sort()
        for score in scores:
            players = self.winners[score]
            self.split_pot(players)
