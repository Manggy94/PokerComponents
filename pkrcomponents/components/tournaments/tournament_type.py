from pkrcomponents.components.utils.common import PokerEnum


class TournamentType(PokerEnum):
    """Class describing the tournament type"""
    CLASSIC = "Multi-Table Tournament", "mtt", "normal"
    KO = "Knockout", "ko"
    FLIGHT = "Flight", "flight"
    SNG = "Sit and Go", "sng", "sitandgo", "sitngo", "sit&go", "Sit&Go"
    SPECIAL = "Special", "special",
    DOUBLE = "Double or Nothing", "don", "doubleornothing"
    HITNRUN = "Hit and Run", "hitnrun", "hit&run", "wys"
    DEGLINGOS = "Deglingos", "deglingos", "madtilt"
    QUALIF = "Qualifier", "qualif", "qualifier"
    WIPT = "Winamax Poker Tour", "wipt", "winamaxpokertour"
    SUPERFREEROLL = "Super Freeroll", "superfreeroll", "freeroll100k"
    SPIN = "Spin&Go", "spin"

    @property
    def name(self):
        return self._name_
