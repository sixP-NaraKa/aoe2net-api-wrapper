from dataclasses import dataclass
from enum import Enum

from .game import Game


@dataclass
class _MappedLeaderboardId:
    aoe2net_id: int
    game: str


class LeaderboardId(Enum):
    """
    A list of available leaderboards and their respective IDs. Note: this list does not include AoE2:HD.
    The corresponding game will be correctly used, depending on the leaderboard ID.
    """

    AOE_ONE_RM = _MappedLeaderboardId(1, Game.AOE_ONE_DE.value)
    AOE_ONE_RM_TEAM = _MappedLeaderboardId(2, Game.AOE_ONE_DE.value)
    AOE_ONE_DM = _MappedLeaderboardId(3, Game.AOE_ONE_DE.value)
    AOE_ONE_DM_TEAM = _MappedLeaderboardId(4, Game.AOE_ONE_DE.value)

    AOE_TWO_UNRANKED = _MappedLeaderboardId(0, Game.AOE_TWO_DE.value)
    AOE_TWO_DM = _MappedLeaderboardId(1, Game.AOE_TWO_DE.value)
    AOE_TWO_DM_TEAM = _MappedLeaderboardId(2, Game.AOE_TWO_DE.value)
    AOE_TWO_RM = _MappedLeaderboardId(3, Game.AOE_TWO_DE.value)
    AOE_TWO_RM_TEAM = _MappedLeaderboardId(4, Game.AOE_TWO_DE.value)
    AOE_TWO_EW = _MappedLeaderboardId(13, Game.AOE_TWO_DE.value)
    AOE_TWO_EW_TEAM = _MappedLeaderboardId(14, Game.AOE_TWO_DE.value)

    AOE_THREE_SUPR = _MappedLeaderboardId(1, Game.AOE_THREE_DE.value)
    AOE_THREE_SUPR_TEAM = _MappedLeaderboardId(2, Game.AOE_THREE_DE.value)
    AOE_THREE_TREATY_ALL = _MappedLeaderboardId(3, Game.AOE_THREE_DE.value)
    AOE_THREE_DM_ALL = _MappedLeaderboardId(4, Game.AOE_THREE_DE.value)

    AOE_FOUR_CUSTOM = _MappedLeaderboardId(0, Game.AOE_FOUR.value)
    AOE_FOUR_QM_1v1 = _MappedLeaderboardId(17, Game.AOE_FOUR.value)
    AOE_FOUR_QM_2v2 = _MappedLeaderboardId(18, Game.AOE_FOUR.value)
    AOE_FOUR_QM_3v3 = _MappedLeaderboardId(19, Game.AOE_FOUR.value)
    AOE_FOUR_QM_4v4 = _MappedLeaderboardId(20, Game.AOE_FOUR.value)


class EventLeaderboardId(Enum):
    """
    A list of available EVENT leaderboards and their respective IDs. Note: this is only related to AoE4.
    The corresponding game will be correctly used, depending on the leaderboard ID used.
    """

    AOE_FOUR_SEASON_ONE = _MappedLeaderboardId(1, Game.AOE_FOUR.value)
    AOE_FOUR_SEASON_TWO = _MappedLeaderboardId(2, Game.AOE_FOUR.value)
    AOE_FOUR_SEASON_THREE = _MappedLeaderboardId(5, Game.AOE_FOUR.value)
    AOE_FOUR_SEASON_THREE_TEAM = _MappedLeaderboardId(6, Game.AOE_FOUR.value)
