# hand_stats

## Overview

This module is part of the `pkrcomponents` package.
## A. Preflop stats
### 1. Flags
Type: *bool*

- **flag_vpip**: Whether the player voluntarily put money in the pot
- **flag_preflop_open_opportunity**: Whether the player had the opportunity to open preflop
- **flag_preflop_open**: Whether the player opened preflop
- **flag_preflop_first_raise**: Whether the player made the first raise preflop
- **flag_preflop_fold**: Whether the player folded preflop
- **flag_preflop_limp**: Whether the player limped preflop
- **flag_preflop_cold_called**: Whether the player cold called preflop
- **flag_preflop_face_raise**: Whether the player faced a raise preflop
- **flag_preflop_bet**: Whether the player bet preflop (Realized at least one raise)
- **flag_preflop_3bet_opportunity**: Whether the player had the opportunity to 3bet preflop
- **flag_preflop_3bet**: Whether the player 3bet preflop
- **flag_preflop_face_3bet**: Whether the player faced a 3bet preflop
- **flag_preflop_4bet_opportunity**: Whether the player had the opportunity to 4+bet preflop
- **flag_preflop_4bet**  Whether the player 4+bet preflop
- **flag_preflop_face_4bet**: Whether the player faced a 4+bet preflop
- **flag_squeeze_opportunity**: Whether the player had the opportunity to squeeze preflop
- **flag_squeeze**: Whether the player squeezed preflop
- **flag_face_squeeze**: Whether the player faced a squeeze preflop
- **flag_steal_opportunity**: Whether the player had the opportunity to steal preflop
- **flag_steal_attempt**: Whether the player attempted to steal preflop
- **flag_face_steal_attempt**: Whether the player faced a steal attempt preflop
- **flag_fold_to_steal_attempt**: Whether the player folded to a steal attempt preflop
- **flag_blind_defense**: Whether the player defended the blinds preflop
- **flag_open_shove**: Whether the player open shoved preflop
- **flag_voluntary_all_in_preflop**: Whether the player went all-in preflop voluntarily
### 2. Counts
Type: *int*

- **count_preflop_player_raises**: The number of raises the player made preflop
- **count_preflop_player_calls**: The number of calls the player made preflop
- **count_faced_limps**: The number of limps the player faced preflop
### 3. Sequences
Type *ActionsSequence*

- **preflop_actions_sequence**: The sequence of actions the player made preflop
### 4. Amounts
Type: *float*

- **amount_preflop_effective_stack**: The effective stack the player had preflop
- **amount_to_call_facing_preflop_bet**: The amount the player had to call facing the preflop blinds
- **amount_to_call_facing_preflop_2bet**: The amount the player had to call facing the preflop 2bet
- **amount_to_call_facing_preflop_3bet**: The amount the player had to call facing the preflop 3bet
- **amount_to_call_facing_preflop_4bet**: The amount the player had to call facing the preflop 4bet
- **amount_first_raise_made_preflop**: The amount the player used on his first raise preflop
- **amount_second_raise_made_preflop**: The amount the player used on his second raise preflop
- **ratio_to_call_facing_preflop_bet**: The ratio of the pot the player had to call facing the preflop bet
- **ratio_to_call_facing_preflop_2bet**: The ratio of the pot the player had to call facing the preflop 2bet
- **ratio_to_call_facing_preflop_3bet**: The ratio of the pot the player had to call facing the preflop 3bet
- **ratio_to_call_facing_preflop_4bet**: The ratio of the pot the player had to call facing the preflop 4bet
- **ratio_first_raise_made_preflop**: The ratio of the pot the player used on his first raise preflop
- **ratio_second_raise_made_preflop**: The ratio of the pot the player used on his second raise preflop
- **total_preflop_bet_amount**: The total amount the player bet preflop
#### 5. Moves
Type: *ActionMove*

- **move_facing_preflop_2bet**: The move the player did when facing a preflop 2bet
- **move_facing_preflop_3bet**: The move the player did when facing a preflop 3bet
- **move_facing_preflop_4bet**: The move the player did when facing a preflop 4bet
- **move_facing_preflop_squeeze**: The move the player did when facing a preflop squeeze
- **move_facing_preflop_steal_attempt**: The move the player did when facing a preflop steal attempt
## B. Flop stats
### 1. Flags
Type: *bool*

- **flag_saw_flop**: Whether the player saw the flop
- **flag_flop_first_to_talk**: Whether the player was the first to talk on the flop
- **flag_flop_has_position**: Whether the player had position on the flop
- **flag_flop_bet**: Whether the player bet on the flop
- **flag_flop_open_opportunity**: Whether the player had the opportunity to open on the flop
- **flag_flop_open**: Whether the player opened on the flop
- **flag_flop_cbet_opportunity**: Whether the player had the opportunity to make a continuation bet on the flop
- **flag_flop_cbet**: Whether the player made a continuation bet on the flop
- **flag_flop_face_cbet**: Whether the player faced a continuation bet on the flop
- **flag_flop_donk_bet_opportunity**: Whether the player had the opportunity to make a donk bet on the flop
- **flag_flop_donk_bet**: Whether the player made a donk bet on the flop
- **flag_flop_face_donk_bet**: Whether the player faced a donk bet on the flop
- **flag_flop_first_raise**: Whether the player made the first raise on the flop
- **flag_flop_fold**: Whether the player folded on the flop
- **flag_flop_check**: Whether the player checked on the flop
- **flag_flop_check_raise**: Whether the player check-raised on the flop
- **flag_flop_face_raise**: Whether the player faced a raise on the flop
- **flag_flop_3bet_opportunity**: Whether the player had the opportunity to 3bet on the flop
- **flag_flop_3bet**: Whether the player 3bet on the flop
- **flag_flop_face_3bet**: Whether the player faced a 3bet on the flop
- **flag_flop_4bet_opportunity**: Whether the player had the opportunity to 4+bet on the flop
- **flag_flop_4bet**: Whether the player 4+bet on the flop
- **flag_flop_face_4bet**: Whether the player faced a 4+bet on the flop
### 2. Counts
Type: *int*

- **count_flop_player_raises**: The number of raises the player made on the flop
- **count_flop_player_calls**: The number of calls the player made on the flop
### 3. Sequences
Type: *ActionsSequence*

- **flop_actions_sequence**: The sequence of actions the player made on the flop
### 4. Amounts
Type: *float*

- **amount_flop_effective_stack**: The effective stack the player had on the flop
- **amount_to_call_facing_flop_bet**: The amount the player had to call facing the flop bet
- **amount_to_call_facing_flop_2bet**: The amount the player had to call facing the flop 2bet
- **amount_to_call_facing_flop_3bet**: The amount the player had to call facing the flop 3bet
- **amount_to_call_facing_flop_4bet**: The amount the player had to call facing the flop 4bet
- **amount_bet_made_flop**: The amount the player used to bet on the flop
- **amount_first_raise_made_flop**: The amount the player used on his first raise on the flop
- **amount_second_raise_made_flop**: The amount the player used on his second raise on the flop
- **ratio_to_call_facing_flop_bet**: The ratio of the pot the player had to call facing the flop bet
- **ratio_to_call_facing_flop_2bet**: The ratio of the pot the player had to call facing the flop 2bet
- **ratio_to_call_facing_flop_3bet**: The ratio of the pot the player had to call facing the flop 3bet
- **ratio_to_call_facing_flop_4bet**: The ratio of the pot the player had to call facing the flop 4bet
- **ratio_bet_made_flop**: The ratio of the pot the player used to bet on the flop
- **ratio_first_raise_made_flop**: The ratio of the pot the player used on his first raise on the flop
- **ratio_second_raise_made_flop**: The ratio of the pot the player used on his second raise on the flop
- **total_flop_bet_amount**: The total amount the player bet on the flop
### 5. Moves
Type: *ActionMove*

- **move_facing_flop_bet**: The move the player did when facing the flop bet
- **move_facing_flop_2bet**: The move the player did when facing the flop 2bet
- **move_facing_flop_3bet**: The move the player did when facing the flop 3bet
- **move_facing_flop_4bet**: The move the player did when facing the flop 4bet
- **move_facing_flop_cbet**: The move the player did when facing the flop cbet
- **move_facing_flop_donk_bet**: The move the player did when facing the flop donk bet
## C. Turn stats
### 1. Flags
Type: *bool*

- **flag_saw_turn**: Whether the player saw the turn
- **flag_turn_first_to_talk**: Whether the player was the first to talk on the turn
- **flag_turn_has_position**: Whether the player had position on the turn
- **flag_turn_bet**: Whether the player bet on the turn
- **flag_turn_open_opportunity**: Whether the player had the opportunity to open on the turn
- **flag_turn_open**: Whether the player opened on the turn
- **flag_turn_cbet_opportunity**: Whether the player had the opportunity to make a continuation bet on the turn
- **flag_turn_cbet**: Whether the player made a continuation bet on the turn
- **flag_turn_face_cbet**: Whether the player faced a continuation bet on the turn
- **flag_turn_donk_bet_opportunity**: Whether the player had the opportunity to make a donk bet on the turn
- **flag_turn_donk_bet**: Whether the player made a donk bet on the turn
- **flag_turn_face_donk_bet**: Whether the player faced a donk bet on the turn
- **flag_turn_first_raise**: Whether the player made the first raise on the turn
- **flag_turn_fold**: Whether the player folded on the turn
- **flag_turn_check**: Whether the player checked on the turn
- **flag_turn_check_raise**: Whether the player check-raised on the turn
- **flag_turn_face_raise**: Whether the player faced a raise on the turn
- **flag_turn_3bet_opportunity**: Whether the player had the opportunity to 3bet on the turn
- **flag_turn_3bet**: Whether the player 3bet on the turn
- **flag_turn_face_3bet**: Whether the player faced a 3bet on the turn
- **flag_turn_4bet_opportunity**: Whether the player had the opportunity to 4+bet on the turn
- **flag_turn_4bet**: Whether the player 4+bet on the turn
- **flag_turn_face_4bet**: Whether the player faced a 4+bet on the turn
### 2. Counts
Type: *int*

- **count_turn_player_raises**: The number of raises the player made on the turn
- **count_turn_player_calls**: The number of calls the player made on the turn
### 3. Sequences
Type: *ActionsSequence*

- **turn_actions_sequence**: The sequence of actions the player made on the turn
### 4. Amounts
Type: *float*

- **amount_turn_effective_stack**: The effective stack the player had on the turn
- **amount_to_call_facing_turn_bet**: The amount the player had to call facing the turn bet
- **amount_to_call_facing_turn_2bet**: The amount the player had to call facing the turn 2bet
- **amount_to_call_facing_turn_3bet**: The amount the player had to call facing the turn 3bet
- **amount_to_call_facing_turn_4bet**: The amount the player had to call facing the turn 4bet
- **amount_bet_made_turn**: The amount the player used to bet on the turn
- **amount_first_raise_made_turn**: The amount the player used on his first raise on the turn
- **amount_second_raise_made_turn**: The amount the player used on his second raise on the turn
- **ratio_to_call_facing_turn_bet**: The ratio of the pot the player had to call facing the turn bet
- **ratio_to_call_facing_turn_2bet**: The ratio of the pot the player had to call facing the turn 2bet
- **ratio_to_call_facing_turn_3bet**: The ratio of the pot the player had to call facing the turn 3bet
- **ratio_to_call_facing_turn_4bet**: The ratio of the pot the player had to call facing the turn 4bet
- **ratio_bet_made_turn**: The ratio of the pot the player used to bet on the turn
- **ratio_first_raise_made_turn**: The ratio of the pot the player used on his first raise on the turn
- **ratio_second_raise_made_turn**: The ratio of the pot the player used on his second raise on the turn
- **total_turn_bet_amount**: The total amount the player bet on the turn
### 5. Moves
Type: *ActionMove*  
- **move_facing_turn_bet**: The move the player did when facing the turn bet
- **move_facing_turn_2bet**: The move the player did when facing the turn 2bet
- **move_facing_turn_3bet**: The move the player did when facing the turn 3bet
- **move_facing_turn_4bet**: The move the player did when facing the turn 4bet
- **move_facing_turn_cbet**: The move the player did when facing the turn cbet
- **move_facing_turn_donk_bet**: The move the player did when facing the turn donk bet
## D. River stats
### 1. Flags
Type: *bool* 

- **flag_saw_river**: Whether the player saw the river
- **flag_river_first_to_talk**: Whether the player was the first to talk on the river
- **flag_river_has_position**: Whether the player had position on the river
- **flag_river_bet**: Whether the player bet on the river
- **flag_river_open_opportunity**: Whether the player had the opportunity to open on the river
- **flag_river_open**: Whether the player opened on the river
- **flag_river_cbet_opportunity**: Whether the player had the opportunity to make a c-bet on the river
- **flag_river_cbet**: Whether the player made a continuation bet on the river
- **flag_river_face_cbet**: Whether the player faced a continuation bet on the river
- **flag_river_donk_bet_opportunity**: Whether the player had the opportunity to make a donk bet on the river
- **flag_river_donk_bet**: Whether the player made a donk bet on the river
- **flag_river_face_donk_bet**: Whether the player faced a donk bet on the river
- **flag_river_first_raise**: Whether the player made the first raise on the river
- **flag_river_fold**: Whether the player folded on the river
- **flag_river_check**: Whether the player checked on the river
- **flag_river_check_raise**: Whether the player check-raised on the river
- **flag_river_face_raise**: Whether the player faced a raise on the river
- **flag_river_3bet_opportunity**: Whether the player had the opportunity to 3bet on the river
- **flag_river_3bet**: Whether the player 3bet on the river
- **flag_river_face_3bet**: Whether the player faced a 3bet on the river
- **flag_river_4bet_opportunity**: Whether the player had the opportunity to 4+bet on the river
- **flag_river_4bet**: Whether the player 4+bet on the river
- **flag_river_face_4bet**: Whether the player faced a 4+bet on the river
### 2. Counts
Type: *int* 

- **count_river_player_raises**: The number of raises the player made on the river
- **count_river_player_calls**: The number of calls the player made on the river
### 3. Sequences
Type: *ActionsSequence*
- **river_actions_sequence**: The sequence of actions the player made on the river
### 4. Amounts
Type: *float*

- **amount_river_effective_stack**: The effective stack the player had on the river
- **amount_to_call_facing_river_bet**: The amount the player had to call facing the river bet
- **amount_to_call_facing_river_2bet**: The amount the player had to call facing the river 2bet
- **amount_to_call_facing_river_3bet**: The amount the player had to call facing the river 3bet
- **amount_to_call_facing_river_4bet**: The amount the player had to call facing the river 4bet
- **amount_bet_made_river**: The amount the player used to bet on the river
- **amount_first_raise_made_river**: The amount the player used on his first raise on the river
- **amount_second_raise_made_river**: The amount the player used on his second raise on the river
- **ratio_to_call_facing_river_bet**: The ratio of the pot the player had to call facing the river bet
- **ratio_to_call_facing_river_2bet**: The ratio of the pot the player had to call facing the river 2bet
- **ratio_to_call_facing_river_3bet**: The ratio of the pot the player had to call facing the river 3bet
- **ratio_to_call_facing_river_4bet**: The ratio of the pot the player had to call facing the river 4bet
- **ratio_bet_made_river**: The ratio of the pot the player used to bet on the river
- **ratio_first_raise_made_river**: The ratio of the pot the player used on his first raise on the river
- **ratio_second_raise_made_river**: The ratio of the pot the player used on his second raise on the river
- **total_river_bet_amount**: The total amount the player bet on the river
### 5. Moves
Type: *ActionMove*

- **move_facing_river_bet**: The move the player did when facing the river bet
- **move_facing_river_2bet**: The move the player did when facing the river 2bet
- **move_facing_river_3bet**: The move the player did when facing the river 3bet
- **move_facing_river_4bet**: The move the player did when facing the river 4bet
- **move_facing_river_cbet**: The move the player did when facing the river cbet
- **move_facing_river_donk_bet**: The move the player did when facing the river donk bet
## E. General stats
### 1. Flags
Types: *bool*

- **flag_is_hero**: Whether the player is the hero
- **flag_won**: Whether the player won the hand
- **flag_went_to_showdown**: Whether the player went to showdown

### 2. Amounts
Types: *float*

- **starting_stack**: The starting stack of the player at the beginning of the hand
- **amount_won**: The amount the player won in the hand
- **total_bet_amount**: The total amount the player bet in the hand
### 3. Moves
Types: *Move*

- **facing_covering_bet_move**: The move the player did when facing a covering bet
- **facing_allin_move**: The move the player did when facing an all-in
### 4. Streets
Types: *Street*

- **fold_street**: The street the player folded
- **all_in_street**: The street the player went all-in
- **face_covering_bet_street**: The street the player faced a covering bet
- **face_allin_street**: The street the player faced an all-in
### 5. Other
- **combo** (*Combo*): The combo the player had

