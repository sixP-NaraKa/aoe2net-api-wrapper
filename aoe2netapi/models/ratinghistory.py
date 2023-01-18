from dataclasses import dataclass
from typing import List, Dict, Union

from dataclasses_json import dataclass_json, Undefined

from aoe2netapi.constants import LeaderboardId, EventLeaderboardId


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RatingHistoryItem:
    rating: int
    num_wins: int
    num_losses: int
    streak: int
    drops: int
    timestamp: str


@dataclass
class RatingHistory:
    game: str
    leaderboard_id: int
    is_event_leaderboard: bool
    ratings: List[RatingHistoryItem]

    def __init__(self,
                 leaderboard_id: Union[LeaderboardId, EventLeaderboardId],
                 is_event_leaderboard: bool,
                 ratings: List[Dict]):
        self.game = leaderboard_id.value.game
        self.leaderboard_id = leaderboard_id.value.aoe2net_id
        self.is_event_leaderboard = is_event_leaderboard
        self.ratings = [RatingHistoryItem.from_dict(rating) for rating in ratings]
