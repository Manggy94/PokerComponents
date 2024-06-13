from itertools import combinations

import numpy as np
from pkrcomponents.constants import ActionMove, Street, Position
from pkrcomponents.card import Card
from pkrcomponents.combo import Combo
from pkrcomponents.hand import Hand
from pkrcomponents.flop import Flop

all_actions = np.hstack(list(ActionMove))
all_cards = np.hstack(list(Card))
all_combos = np.hstack(list(Combo))
all_hands = np.hstack(list(Hand))
all_positions = np.hstack(list(Position))
all_streets = np.hstack(list(Street))
str_actions = all_actions.astype(str)
str_positions = all_positions.astype(str)
str_combos = all_combos.astype(str)
str_hands = all_hands.astype(str)
str_streets = all_streets.astype(str)
all_flops = np.hstack(list(Flop))

players_positions = {
    1: [Position.BB],
    2: [Position.SB, Position.BB],
    3: [Position.BTN, Position.SB, Position.BB],
    4: [Position.CO, Position.BTN, Position.SB, Position.BB],
    5: [Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
    6: [Position.UTG, Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
    7: [Position.UTG, Position.UTG1, Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
    8: [Position.UTG, Position.UTG1, Position.UTG2, Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
    9: [Position.UTG, Position.UTG1, Position.UTG2, Position.UTG3, Position.HJ, Position.CO, Position.BTN, Position.SB,
        Position.BB]


}
