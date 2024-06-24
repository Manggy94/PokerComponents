from pkrcomponents.players.position import Position


class PositionsMapMeta(type):
    def __new__(mcs, clsname, bases, classdict):
        """Cache PositionsMap instances on the class itself, taken from Position"""
        cls = super(PositionsMapMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls.all_positions_maps = list(
            cls(positions_list=positions_list)
            for positions_list in Position.get_maps()
        )
        return cls

    def __iter__(cls):
        return iter(cls.all_positions_maps)

    def __len__(cls):
        return len(cls.all_positions_maps)
