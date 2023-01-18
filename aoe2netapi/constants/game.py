from enum import Enum, EnumMeta


class _GameEnumMeta(EnumMeta):
    def __contains__(self, item) -> bool:
        return isinstance(item, Game)


class Game(Enum, metaclass=_GameEnumMeta):
    """ A list of available AoE games. """

    AOE_ONE_DE = "aoe1de"
    AOE_TWO_HD = "aoe2hd"
    AOE_TWO_DE = "aoe2de"
    AOE_THREE_DE = "aoe3de"
    AOE_FOUR = "aoe4"
