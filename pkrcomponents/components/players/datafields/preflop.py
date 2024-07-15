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
FLAG_OPEN_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to open ', 'type': 'bool'})
FLAG_OPEN = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player opened ', 'type': 'bool'})
FLAG_FIRST_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player made the first raise ', 'type': 'bool'})
FLAG_FOLD = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player folded ', 'type': 'bool'})
FLAG_LIMP = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player limped ', 'type': 'bool'})
FLAG_COLD_CALLED = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player cold called ', 'type': 'bool'})
FLAG_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player raised ', 'type': 'bool'})
FLAG_RAISE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to raise ', 'type': 'bool'})
FLAG_FACE_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a raise ', 'type': 'bool'})
FLAG_3BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to 3bet ', 'type': 'bool'})
FLAG_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player 3bet ', 'type': 'bool'})
FLAG_FACE_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a 3bet ', 'type': 'bool'})
FLAG_4BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to 4+bet ', 'type': 'bool'})
FLAG_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player 4+bet ', 'type': 'bool'})
FLAG_FACE_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a 4+bet ', 'type': 'bool'})
FLAG_SQUEEZE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to squeeze ', 'type': 'bool'})
FLAG_SQUEEZE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player squeezed ', 'type': 'bool'})
FLAG_FACE_SQUEEZE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a squeeze ', 'type': 'bool'})
FLAG_STEAL_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to steal ', 'type': 'bool'})
FLAG_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player attempted to steal ', 'type': 'bool'})
FLAG_FACE_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player faced a steal attempt ', 'type': 'bool'})
FLAG_FOLD_TO_STEAL_ATTEMPT = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player folded to a steal attempt ', 'type': 'bool'})
FLAG_BLIND_DEFENSE_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player had the opportunity to defend the blinds ', 'type': 'bool'})
FLAG_BLIND_DEFENSE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player defended the blinds ', 'type': 'bool'})
FLAG_OPEN_SHOVE = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player open shoved ', 'type': 'bool'})
FLAG_VOLUNTARY_ALL_IN = field(
    default=False, validator=instance_of(bool),
    metadata={'description': 'Whether the player voluntarily went all in ', 'type': 'bool'})
# 2. Counts
COUNT_PLAYER_RAISES = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of raises the player made ', 'type': 'tiny_int+'})
COUNT_PLAYER_CALLS = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of calls the player made ', 'type': 'tiny_int+'})
COUNT_FACED_LIMPS = field(
    default=0, validator=instance_of(int),
    metadata={'description': 'The number of limps the player faced ', 'type': 'tiny_int+'})
# 3. Sequences
ACTIONS_SEQUENCE = field(
    default=None, validator=optional(instance_of(ActionsSequence)),
    metadata={'description': 'The sequence of actions the player made ', 'type': 'ActionsSequence'})
# 4. Amounts
AMOUNT_EFFECTIVE_STACK = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The effective stack the player had ', 'type': 'decimal_15_2'})
AMOUNT_TO_CALL_FACING_1BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the  big blind', 'type': 'decimal_15_2'})
AMOUNT_TO_CALL_FACING_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the  2bet', 'type': 'decimal_15_2'})
AMOUNT_TO_CALL_FACING_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the  3bet', 'type': 'decimal_15_2'})
AMOUNT_TO_CALL_FACING_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player had to call facing the  4bet', 'type': 'decimal_15_2'})
AMOUNT_FIRST_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player used on his first raise ', 'type': 'decimal_15_2'})
AMOUNT_SECOND_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The amount the player used on his second raise ', 'type': 'decimal_15_2'})
RATIO_TO_CALL_FACING_1BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the bb', 'type': 'decimal_10_5'})
RATIO_TO_CALL_FACING_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the  2bet', 'type': 'decimal_10_5'})
RATIO_TO_CALL_FACING_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the  3bet', 'type': 'decimal_10_5'})
RATIO_TO_CALL_FACING_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player had to call facing the  4bet', 'type': 'decimal_10_5'})
RATIO_FIRST_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player used on his first raise ', 'type': 'decimal_10_5'})
RATIO_SECOND_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The ratio of the pot the player used on his second raise ', 'type': 'decimal_10_5'})
TOTAL_BET_AMOUNT = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={'description': 'The total amount the player bet ', 'type': 'decimal_15_2'})
# 5. Moves
MOVE_FACING_2BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a 2bet', 'type': 'ActionMove'})
MOVE_FACING_3BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a 3bet', 'type': 'ActionMove'})
MOVE_FACING_4BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a 4bet', 'type': 'ActionMove'})
MOVE_FACING_SQUEEZE = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a squeeze', 'type': 'ActionMove'})
MOVE_FACING_STEAL_ATTEMPT = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={'description': 'The move the player did when facing a steal attempt', 'type': 'ActionMove'})

PREFLOP_FIELDS = list({"field_name": field_name, "field_var": field_var}
                      for field_name, field_var in locals().items() if field_name.isupper())
