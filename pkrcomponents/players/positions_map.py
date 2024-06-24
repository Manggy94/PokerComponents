from pkrcomponents.players.position import Position
from pkrcomponents.utils.common import _ReprMixin
from pkrcomponents.utils.meta.positions_map_meta import PositionsMapMeta


class PositionsMap(_ReprMixin, metaclass=PositionsMapMeta):
    def __init__(self, positions_list: list[Position]):
        self.positions = positions_list

    def __str__(self):
        return (f"{self.cnt_players}"
                f"{'-BTN' if self.has_btn else ''}"
                f"{'-SB' if self.has_sb else ''}"
                f"{'-BB' if self.has_bb else ''}")

    @property
    def cnt_players(self):
        return len(self.positions)

    @property
    def has_sb(self):
        return Position.SB in self.positions

    @property
    def has_bb(self):
        return Position.BB in self.positions

    @property
    def has_btn(self):
        return Position.BTN in self.positions
