from attrs import field, Factory
from attrs.validators import instance_of, ge, optional
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.combo import Combo

# 1. Flags
FLAG_WENT_TO_SHOWDOWN = field(
    default=False, validator=[instance_of(bool)],
    metadata={
        'description': 'Whether the player went to showdown',
        'type': 'bool'})
FLAG_IS_HERO = field(
    default=False, validator=[instance_of(bool)],
    metadata={
        'description': 'Whether the player is the hero',
        'type': 'bool'})
FLAG_WON_HAND = field(
    default=False, validator=[instance_of(bool)],
    metadata={
        'description': 'Whether the player won the hand',
        'type': 'bool'})
# 2. Amounts
STARTING_STACK = field(
    default=0, validator=[ge(0), instance_of(float)], converter=float,
    metadata={
        'description': 'The starting stack of the player at the beginning of the hand',
        'type': 'float'})
AMOUNT_WON = field(
    default=0, validator=[ge(0), instance_of(float)], converter=float,
    metadata={
        'description': 'The amount the player won in the hand',
        'type': 'float'})
AMOUNT_EXPECTED_WON = field(
    default=0, validator=[ge(0), instance_of(float)], converter=float,
    metadata={
        'description': 'The amount the player is expected to win in the hand when all combos are revealed (EV)',
        'type': 'float'})
TOTAL_BET_AMOUNT = field(
    default=0, validator=[ge(0), instance_of(float)], converter=float,
    metadata={
        'description': 'The total amount the player bet in the hand',
        'type': 'float'})
# 3. Moves
FACING_COVERING_BET_MOVE = field(
    default=None, validator=[optional(instance_of(ActionMove))],
    metadata={
        'description': 'The move the player did when facing a covering bet',
        'type': 'ActionMove'})
FACING_ALL_IN_MOVE = field(
    default=None, validator=[optional(instance_of(ActionMove))],
    metadata={
        'description': 'The move the player did when facing an all-in',
        'type': 'ActionMove'})
# 4. Streets
FOLD_STREET = field(
    default=None, validator=[optional(instance_of(Street))],
    metadata={
        'description': 'The street the player folded',
        'type': 'Street'})
ALL_IN_STREET = field(
    default=None, validator=[optional(instance_of(Street))],
    metadata={
        'description': 'The street the player went all-in',
        'type': 'Street'})
FACE_COVERING_BET_STREET = field(
    default=None, validator=[optional(instance_of(Street))],
    metadata={
        'description': 'The street the player faced a covering bet',
        'type': 'Street'})
FACE_ALL_IN_STREET = field(
    default=None, validator=[optional(instance_of(Street))],
    metadata={
        'description': 'The street the player faced an all-in',
        'type': 'Street'})
# 5. Other
COMBO = field(
    default=None, validator=[optional(instance_of(Combo))],
    metadata={
        'description': 'The combo the player had',
        'type': 'Combo'})
