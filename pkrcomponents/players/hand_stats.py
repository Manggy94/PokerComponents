from attrs import define, field
from attrs.validators import instance_of, ge


@define
class HandStats:
    """
    This class represents the statistics of a player's hand in a poker game
    Attributes:
        flag_vpip (bool): Whether the player voluntarily put money in the pot
        flag_preflop_open_opportunity (bool): Whether the player had the opportunity to open preflop
        flag_preflop_opened (bool): Whether the player opened preflop
        flag_preflop_first_raise (bool): Whether the player made the first raise preflop
        flag_preflop_fold (bool): Whether the player folded preflop
        flag_preflop_limp (bool): Whether the player limped preflop
        flag_preflop_cold_called (bool): Whether the player cold called preflop
        flag_preflop_face_raise (bool): Whether the player faced a raise preflop
        flag_preflop_3bet_opportunity (bool): Whether the player had the opportunity to 3bet preflop
        flag_preflop_3bet (bool): Whether the player 3bet preflop
        flag_preflop_face_3bet (bool): Whether the player faced a 3bet preflop
        flag_preflop_4bet_opportunity (bool): Whether the player had the opportunity to 4+bet preflop
        flag_preflop_4bet (bool): Whether the player 4+bet preflop
        flag_preflop_face_4bet (bool): Whether the player faced a 4+bet preflop
        count_preflop_player_raises (int): The number of raises the player made preflop
        count_preflop_player_calls (int): The number of calls the player made preflop
    """

    flag_vpip = field(default=False, validator=instance_of(bool), metadata={'description': 'Whether the player voluntarily put money in the pot'})
    flag_preflop_open_opportunity = field(default=False, validator=instance_of(bool), metadata={'description': 'Whether the player had the opportunity to open preflop'})
    flag_preflop_opened = field(default=False, validator=instance_of(bool), metadata={'description': 'Whether the player opened preflop'})
    flag_preflop_first_raise = field(default=False, validator=instance_of(bool))
    flag_preflop_fold = field(default=False, validator=instance_of(bool))
    flag_preflop_limp = field(default=False, validator=instance_of(bool))
    flag_preflop_cold_called = field(default=False, validator=instance_of(bool))
    flag_preflop_face_raise = field(default=False, validator=instance_of(bool))
    flag_preflop_3bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_preflop_3bet = field(default=False, validator=instance_of(bool))
    flag_preflop_face_3bet = field(default=False, validator=instance_of(bool))
    flag_preflop_4bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_preflop_4bet = field(default=False, validator=instance_of(bool))
    flag_preflop_face_4bet = field(default=False, validator=instance_of(bool))
    count_preflop_player_raises = field(default=0, validator=ge(0))
    count_preflop_player_calls = field(default=0, validator=ge(0))

    def reset(self):
        """
        Resets the statistics
        """
        self.flag_vpip = False
        self.flag_preflop_open_opportunity = False
        self.flag_preflop_opened = False
        self.flag_preflop_first_raise = False
        self.flag_preflop_fold = False
        self.flag_preflop_limp = False
        self.flag_preflop_cold_called = False
        self.flag_preflop_face_raise = False
        self.flag_preflop_3bet_opportunity = False
        self.flag_preflop_3bet = False
        self.flag_preflop_face_3bet = False
        self.flag_preflop_4bet_opportunity = False
        self.flag_preflop_4bet = False
        self.flag_preflop_face_4bet = False
        self.count_preflop_player_raises = 0
        self.count_preflop_player_calls = 0

