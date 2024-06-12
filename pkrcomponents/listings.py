from itertools import combinations

import numpy as np
from pkrcomponents.constants import ActionMove, Street, Position
from pkrcomponents.card import Card
from pkrcomponents.hand import Hand
from pkrcomponents.board import Flop

all_actions = np.hstack(list(ActionMove))
all_cards = np.hstack(list(Card))
all_combos = np.hstack([hand.to_combos() for hand in list(Hand)])
all_hands = np.hstack(list(Hand))
all_positions = np.hstack([position for position in list(Position)])
all_streets = np.hstack(list(Street))
str_actions = all_actions.astype(str)
str_positions = all_positions.astype(str)
str_combos = all_combos.astype(str)
str_hands = all_hands.astype(str)
str_streets = all_streets.astype(str)
all_flops = list(
    Flop(
        first_card=flop_cards[0],
        second_card=flop_cards[1],
        third_card=flop_cards[2]
    )
    for flop_cards in list(combinations(all_cards, 3))
)

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

