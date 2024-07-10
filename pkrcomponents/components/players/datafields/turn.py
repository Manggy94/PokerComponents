from attrs import field, Factory
from attrs.validators import instance_of, ge, optional
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.actions.action_move import ActionMove

# 1. Flags
FLAG_SAW_TURN = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player saw the turn",
        "type": "bool"})
FLAG_TURN_FIRST_TO_TALK = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player was the first to talk on the turn",
        "type": "bool"})
FLAG_TURN_HAS_POSITION = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had position on the turn",
        "type": "bool"})
FLAG_TURN_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player bet on the turn",
        "type": "bool"})
FLAG_TURN_OPEN_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to open on the turn",
        "type": "bool"})
FLAG_TURN_OPEN = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player opened on the turn",
        "type": "bool"})
FLAG_TURN_CBET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to make a continuation bet on the turn",
        "type": "bool"})
FLAG_TURN_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made a continuation bet on the turn",
        "type": "bool"})
FLAG_TURN_FACE_CBET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a continuation bet on the turn",
        "type": "bool"})
FLAG_TURN_DONK_BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to make a donk bet on the turn",
        "type": "bool"})
FLAG_TURN_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made a donk bet on the turn",
        "type": "bool"})
FLAG_TURN_FACE_DONK_BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a donk bet on the turn",
        "type": "bool"})
FLAG_TURN_FIRST_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player made the first raise on the turn",
        "type": "bool"})
FLAG_TURN_FOLD = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player folded on the turn",
        "type": "bool"})
FLAG_TURN_CHECK = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player checked on the turn",
        "type": "bool"})
FLAG_TURN_CHECK_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player check-raised on the turn",
        "type": "bool"})
FLAG_TURN_FACE_RAISE = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a raise on the turn",
        "type": "bool"})
FLAG_TURN_3BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to 3bet on the turn",
        "type": "bool"})
FLAG_TURN_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player 3bet on the turn",
        "type": "bool"})
FLAG_TURN_FACE_3BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a 3bet on the turn",
        "type": "bool"})
FLAG_TURN_4BET_OPPORTUNITY = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player had the opportunity to 4+bet on the turn",
        "type": "bool"})
FLAG_TURN_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player 4+bet on the turn",
        "type": "bool"})
FLAG_TURN_FACE_4BET = field(
    default=False, validator=instance_of(bool),
    metadata={
        "description": "Whether the player faced a 4+bet on the turn",
        "type": "bool"})
# 2. Counts
COUNT_TURN_PLAYER_RAISES = field(
    default=0, validator=instance_of(int),
    metadata={
        "description": "The number of raises the player made on the turn",
        "type": "int"})
COUNT_TURN_PLAYER_CALLS = field(
    default=0, validator=instance_of(int),
    metadata={
        "description": "The number of calls the player made on the turn",
        "type": "int"})
# 3. Sequences
TURN_ACTIONS_SEQUENCE = field(
    default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence),
    metadata={
        "description": "The sequence of actions the player made on the turn",
        "type": "ActionsSequence"})
# 4. Amounts
AMOUNT_TURN_EFFECTIVE_STACK = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The effective stack the player had on the turn",
        "type": "float"})
AMOUNT_TO_CALL_FACING_TURN_BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player had to call facing the turn bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_TURN_2BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player had to call facing the turn 2bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_TURN_3BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player had to call facing the turn 3bet",
        "type": "float"})
AMOUNT_TO_CALL_FACING_TURN_4BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player had to call facing the turn 4bet",
        "type": "float"})
AMOUNT_BET_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player used to bet on the turn",
        "type": "float"})
AMOUNT_FIRST_RAISE_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player used on his first raise on the turn",
        "type": "float"})
AMOUNT_SECOND_RAISE_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The amount the player used on his second raise on the turn",
        "type": "float"})
RATIO_TO_CALL_FACING_TURN_BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the turn bet",
        "type": "float"})
RATIO_TO_CALL_FACING_TURN_2BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the turn 2bet",
        "type": "float"})
RATIO_TO_CALL_FACING_TURN_3BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the turn 3bet",
        "type": "float"})
RATIO_TO_CALL_FACING_TURN_4BET = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player had to call facing the turn 4bet",
        "type": "float"})
RATIO_BET_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player used to bet on the turn",
        "type": "float"})
RATIO_FIRST_RAISE_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player used on his first raise on the turn",
        "type": "float"})
RATIO_SECOND_RAISE_MADE_TURN = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The ratio of the pot the player used on his second raise on the turn",
        "type": "float"})
TOTAL_TURN_BET_AMOUNT = field(
    default=0.0, validator=instance_of(float), converter=float,
    metadata={
        "description": "The total amount the player bet on the turn",
        "type": "float"})
# 5. Moves
MOVE_FACING_TURN_BET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn bet",
        "type": "ActionMove"})
MOVE_FACING_TURN_2BET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn 2bet",
        "type": "ActionMove"})
MOVE_FACING_TURN_3BET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn 3bet",
        "type": "ActionMove"})
MOVE_FACING_TURN_4BET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn 4bet",
        "type": "ActionMove"})
MOVE_FACING_TURN_CBET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn cbet",
        "type": "ActionMove"})
MOVE_FACING_TURN_DONK_BET = field(
    default=None,
    metadata={
        "description": "The move the player did when facing the turn donk bet",
        "type": "ActionMove"})

