import numpy as np
from pkrcomponents.constants import Action, Street, Position
from pkrcomponents.card import Card
from pkrcomponents.hand import Hand

all_actions = np.hstack(list(Action))
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

players_positions = {
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

print(all_hands)