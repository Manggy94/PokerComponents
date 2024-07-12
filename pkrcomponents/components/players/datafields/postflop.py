# B. Flop stats
# 1. Flags
from attrs import field, Factory
from attrs.validators import instance_of, optional
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.actions.action_move import ActionMove

# 1. Flags
FLAG_SAW = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player saw the flop',
        'type': 'bool'})
FLAG_FIRST_TO_TALK = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player was the first to talk on the street',
        'type': 'bool'})
FLAG_HAS_POSITION = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had position on the street',
        'type': 'bool'})
FLAG_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player bet on the street',
        'type': 'bool'})
FLAG_OPEN_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had the opportunity to open on the street',
        'type': 'bool'})
FLAG_OPEN = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player opened on the street',
        'type': 'bool'})
FLAG_CBET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had the opportunity to make a continuation bet on the street',
        'type': 'bool'})
FLAG_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player made a continuation bet on the street',
        'type': 'bool'})
FLAG_FACE_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player faced a continuation bet on the street',
        'type': 'bool'})
FLAG_DONK_BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had the opportunity to make a donk bet on the street',
        'type': 'bool'})
FLAG_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player made a donk bet on the street',
        'type': 'bool'})
FLAG_FACE_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player faced a donk bet on the street',
        'type': 'bool'})
FLAG_FIRST_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player made the first raise on the street',
        'type': 'bool'})
FLAG_FOLD = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player folded on the street',
        'type': 'bool'})
FLAG_CHECK = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player checked on the street',
        'type': 'bool'})
FLAG_CHECK_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player check-raised on the street',
        'type': 'bool'})
FLAG_FACE_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player faced a raise on the street',
        'type': 'bool'})
FLAG_3BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had the opportunity to 3bet on the street',
        'type': 'bool'})
FLAG_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player 3bet on the street',
        'type': 'bool'})
FLAG_FACE_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player faced a 3bet on the street',
        'type': 'bool'})
FLAG_4BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player had the opportunity to 4+bet on the street',
        'type': 'bool'})
FLAG_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player 4+bet on the street',
        'type': 'bool'})
FLAG_FACE_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        'description': 'Whether the player faced a 4+bet on the street',
        'type': 'bool'})
# 2. Counts
COUNT_PLAYER_RAISES = field(
    default=0, validator=instance_of(int),
    metadata={
        'description': 'The number of raises the player made on the street',
        'type': 'int'})
COUNT_PLAYER_CALLS = field(
    default=0, validator=instance_of(int),
    metadata={
        'description': 'The number of calls the player made on the street',
        'type': 'int'})
# 3. Sequences
ACTIONS_SEQUENCE = field(
    default=Factory(lambda: ActionsSequence()), validator=optional(instance_of(ActionsSequence)),
    metadata={
        'description': 'The sequence of actions the player made on the street',
        'type': 'ActionsSequence'})
# 4. Amounts
AMOUNT_EFFECTIVE_STACK = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The effective stack the player had on the street',
        'type': 'float'})
AMOUNT_TO_CALL_FACING_BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player had to call facing the street bet',
        'type': 'float'})
AMOUNT_TO_CALL_FACING_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player had to call facing the street 2bet',
        'type': 'float'})
AMOUNT_TO_CALL_FACING_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player had to call facing the street 3bet',
        'type': 'float'})
AMOUNT_TO_CALL_FACING_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player had to call facing the street 4bet',
        'type': 'float'})
AMOUNT_BET_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player used to bet on the street',
        'type': 'float'})
AMOUNT_FIRST_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player used on his first raise on the street',
        'type': 'float'})
AMOUNT_SECOND_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The amount the player used on his second raise on the street',
        'type': 'float'})
RATIO_TO_CALL_FACING_BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player had to call facing the street bet',
        'type': 'float'})
RATIO_TO_CALL_FACING_2BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player had to call facing the street 2bet',
        'type': 'float'})
RATIO_TO_CALL_FACING_3BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player had to call facing the street 3bet',
        'type': 'float'})
RATIO_TO_CALL_FACING_4BET = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player had to call facing the street 4bet',
        'type': 'float'})
RATIO_BET_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player used to bet on the street',
        'type': 'float'})
RATIO_FIRST_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player used on his first raise on the street',
        'type': 'float'})
RATIO_SECOND_RAISE_MADE = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The ratio of the pot the player used on his second raise on the street',
        'type': 'float'})
TOTAL_BET_AMOUNT = field(
    default=0, validator=instance_of(float), converter=float,
    metadata={
        'description': 'The total amount the player bet on the street',
        'type': 'float'})
# 5. Moves
MOVE_FACING_BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street bet',
        'type': 'ActionMove'})
MOVE_FACING_2BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street 2bet',
        'type': 'ActionMove'})
MOVE_FACING_3BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street 3bet',
        'type': 'ActionMove'})
MOVE_FACING_4BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street 4bet',
        'type': 'ActionMove'})
MOVE_FACING_CBET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street cbet',
        'type': 'ActionMove'})
MOVE_FACING_DONK_BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        'description': 'The move the player did when facing the street donk bet',
        'type': 'ActionMove'})
