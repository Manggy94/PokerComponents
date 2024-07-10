from attrs import field, Factory
from attrs.validators import instance_of, ge, optional
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.actions.action_move import ActionMove

# 1. Flags
FLAG_SAW_RIVER = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player saw the river",
        "type": "bool"})
FLAG_RIVER_FIRST_TO_TALK = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player was the first to talk on the river",
        "type": "bool"})
FLAG_RIVER_HAS_POSITION = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had position on the river",
        "type": "bool"})
FLAG_RIVER_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player bet on the river",
        "type": "bool"})
FLAG_RIVER_OPEN_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to open on the river",
        "type": "bool"})
FLAG_RIVER_OPEN = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player opened on the river",
        "type": "bool"})
FLAG_RIVER_CBET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to make a c-bet on the river",
        "type": "bool"})
FLAG_RIVER_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made a continuation bet on the river",
        "type": "bool"})
FLAG_RIVER_FACE_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a continuation bet on the river",
        "type": "bool"})
FLAG_RIVER_DONK_BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to make a donk bet on the river",
        "type": "bool"})
FLAG_RIVER_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made a donk bet on the river",
        "type": "bool"})
FLAG_RIVER_FACE_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a donk bet on the river",
        "type": "bool"})
FLAG_RIVER_FIRST_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made the first raise on the river",
        "type": "bool"})
FLAG_RIVER_FOLD = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player folded on the river",
        "type": "bool"})
FLAG_RIVER_CHECK = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player checked on the river",
        "type": "bool"})
FLAG_RIVER_CHECK_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player check-raised on the river",
        "type": "bool"})
FLAG_RIVER_FACE_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a raise on the river",
        "type": "bool"})
FLAG_RIVER_3BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to 3bet on the river",
        "type": "bool"})
FLAG_RIVER_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player 3bet on the river",
        "type": "bool"})
FLAG_RIVER_FACE_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a 3bet on the river",
        "type": "bool"})
FLAG_RIVER_4BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to 4+bet on the river",
        "type": "bool"})
FLAG_RIVER_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player 4+bet on the river",
        "type": "bool"})
FLAG_RIVER_FACE_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a 4+bet on the river",
        "type": "bool"})
# 2. Counts
COUNT_RIVER_PLAYER_RAISES = field(
    default=0, validator=ge(0),
    metadata={
        "description": "The number of raises the player made on the river",
        "type": "int"})
COUNT_RIVER_PLAYER_CALLS = field(
    default=0, validator=ge(0),
    metadata={
        "description": "The number of calls the player made on the river",
        "type": "int"})
# 3. Sequences
RIVER_ACTIONS_SEQUENCE = field(
    default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence),
    metadata={
        "description": "The sequence of actions the player made on the river",
        "type": "ActionsSequence"})
# 4. Amounts
AMOUNT_RIVER_EFFECTIVE_STACK = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The effective stack the player had on the river",
        "type": "float"})
AMOUNT_TO_CALL_FACING_RIVER_BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player had to call facing the river bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_RIVER_2BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player had to call facing the river 2bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_RIVER_3BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player had to call facing the river 3bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_RIVER_4BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player had to call facing the river 4bet",
        "type": "float"})
AMOUNT_BET_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player used to bet on the river",
        "type": "float"})
AMOUNT_FIRST_RAISE_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player used on his first raise on the river",
        "type": "float"})
AMOUNT_SECOND_RAISE_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The amount the player used on his second raise on the river",
        "type": "float"})
RATIO_TO_CALL_FACING_RIVER_BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the river bet",
        "type": "float"})
RATIO_TO_CALL_FACING_RIVER_2BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the river 2bet",
        "type": "float"})
RATIO_TO_CALL_FACING_RIVER_3BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the river 3bet",
        "type": "float"})
RATIO_TO_CALL_FACING_RIVER_4BET = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the river 4bet",
        "type": "float"})
RATIO_BET_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player used to bet on the river",
        "type": "float"})
RATIO_FIRST_RAISE_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player used on his first raise on the river",
        "type": "float"})
RATIO_SECOND_RAISE_MADE_RIVER = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The ratio of the pot the player used on his second raise on the river",
        "type": "float"})
TOTAL_RIVER_BET_AMOUNT = field(
    default=0, validator=ge(0), converter=float,
    metadata={
        "description": "The total amount the player bet on the river",
        "type": "float"})
# 5. Moves
MOVE_FACING_RIVER_BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river bet",
        "type": "ActionMove"})
MOVE_FACING_RIVER_2BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river 2bet",
        "type": "ActionMove"})
MOVE_FACING_RIVER_3BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river 3bet",
        "type": "ActionMove"})
MOVE_FACING_RIVER_4BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river 4bet",
        "type": "ActionMove"})
MOVE_FACING_RIVER_CBET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river cbet",
        "type": "ActionMove"})
MOVE_FACING_RIVER_DONK_BET = field(
    default=None, validator=optional(instance_of(ActionMove)),
    metadata={
        "description": "The move the player did when facing the river donk bet",
        "type": "ActionMove"})

