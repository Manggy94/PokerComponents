"""
This module contains the data fields for the preflop hand stats of a player.
"""
from attrs import field, Factory
from attrs.validators import instance_of, optional
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.actions_sequence import ActionsSequence

# 1. Flags
FLAG_VPIP = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player voluntarily put money in the pot', 'type': 'bool'})
FLAG_PREFLOP_OPEN_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to open preflop', 'type': 'bool'})
FLAG_PREFLOP_OPEN = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player opened preflop', 'type': 'bool'})
FLAG_PREFLOP_FIRST_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player made the first raise preflop', 'type': 'bool'})
FLAG_PREFLOP_FOLD = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player folded preflop', 'type': 'bool'})
FLAG_PREFLOP_LIMP = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player limped preflop', 'type': 'bool'})
FLAG_PREFLOP_COLD_CALLED = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player cold called preflop', 'type': 'bool'})
FLAG_PREFLOP_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player raised preflop', 'type': 'bool'})
FLAG_PREFLOP_RAISE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to raise preflop', 'type': 'bool'})
FLAG_PREFLOP_FACE_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a raise preflop', 'type': 'bool'})
FLAG_PREFLOP_3BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to 3bet preflop', 'type': 'bool'})
FLAG_PREFLOP_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player 3bet preflop', 'type': 'bool'})
FLAG_PREFLOP_FACE_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a 3bet preflop', 'type': 'bool'})
FLAG_PREFLOP_4BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to 4+bet preflop', 'type': 'bool'})
FLAG_PREFLOP_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player 4+bet preflop', 'type': 'bool'})
FLAG_PREFLOP_FACE_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a 4+bet preflop', 'type': 'bool'})
FLAG_SQUEEZE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to squeeze preflop', 'type': 'bool'})
FLAG_SQUEEZE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player squeezed preflop', 'type': 'bool'})
FLAG_FACE_SQUEEZE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a squeeze preflop', 'type': 'bool'})
FLAG_STEAL_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to steal preflop', 'type': 'bool'})
FLAG_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player attempted to steal preflop', 'type': 'bool'})
FLAG_FACE_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a steal attempt preflop', 'type': 'bool'})
FLAG_FOLD_TO_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player folded to a steal attempt preflop', 'type': 'bool'})
FLAG_BLIND_DEFENSE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to defend the blinds preflop', 'type': 'bool'})
FLAG_BLIND_DEFENSE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player defended the blinds preflop', 'type': 'bool'})
FLAG_OPEN_SHOVE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player open shoved preflop', 'type': 'bool'})
FLAG_VOLUNTARY_ALL_IN_PREFLOP = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player voluntarily went all in preflop', 'type': 'bool'})
# 2. Counts
COUNT_PREFLOP_PLAYER_RAISES = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of raises the player made preflop', 'type': 'int'})
COUNT_PREFLOP_PLAYER_CALLS = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of calls the player made preflop', 'type': 'int'})
COUNT_FACED_LIMPS = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of limps the player faced preflop', 'type': 'int'})
# 3. Sequences
PREFLOP_ACTIONS_SEQUENCE = field(
    default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence),
    metadata={'description': 'The sequence of actions the player made preflop', 'type': 'ActionsSequence'})
# 4. Amounts
AMOUNT_PREFLOP_EFFECTIVE_STACK = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The effective stack the player had preflop', 'type': 'float'})
AMOUNT_TO_CALL_FACING_PREFLOP_BB = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the preflop big blind', 'type': 'float'})
AMOUNT_TO_CALL_FACING_PREFLOP_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the preflop 2bet', 'type': 'float'})
AMOUNT_TO_CALL_FACING_PREFLOP_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the preflop 3bet', 'type': 'float'})
AMOUNT_TO_CALL_FACING_PREFLOP_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the preflop 4bet', 'type': 'float'})
AMOUNT_FIRST_RAISE_MADE_PREFLOP = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player used on his first raise preflop', 'type': 'float'})
AMOUNT_SECOND_RAISE_MADE_PREFLOP = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player used on his second raise preflop', 'type': 'float'})
RATIO_TO_CALL_FACING_PREFLOP_BB = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the bb', 'type': 'float'})
RATIO_TO_CALL_FACING_PREFLOP_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the preflop 2bet', 'type': 'float'})
RATIO_TO_CALL_FACING_PREFLOP_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the preflop 3bet', 'type': 'float'})
RATIO_TO_CALL_FACING_PREFLOP_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the preflop 4bet', 'type': 'float'})
RATIO_FIRST_RAISE_MADE_PREFLOP = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player used on his first raise preflop', 'type': 'float'})
RATIO_SECOND_RAISE_MADE_PREFLOP = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player used on his second raise preflop', 'type': 'float'})
TOTAL_PREFLOP_BET_AMOUNT = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The total amount the player bet preflop', 'type': 'float'})
# 5. Moves
MOVE_FACING_PREFLOP_2BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a preflop 2bet', 'type': 'ActionMove'})
MOVE_FACING_PREFLOP_3BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a preflop 3bet', 'type': 'ActionMove'})
MOVE_FACING_PREFLOP_4BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a preflop 4bet', 'type': 'ActionMove'})
MOVE_FACING_SQUEEZE = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a preflop squeeze', 'type': 'ActionMove'})
MOVE_FACING_STEAL_ATTEMPT = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a preflop steal attempt', 'type': 'ActionMove'})

PREFLOP_FIELDS = list({"field_name": field_name, "field_var": field_var}
                      for field_name, field_var in locals().items() if field_name.isupper())
