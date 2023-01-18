from dataclasses import dataclass, field
from typing import List, Optional, Any

from dataclasses_json import dataclass_json, Undefined, config


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LeaderboardPlayer:
    profile_id: str
    rank: int
    rating: int
    steam_id: str
    icon: Optional[Any]
    name: str
    clan: Optional[str]
    country: Optional[str]
    previous_rating: int
    highest_rating: int
    streak: Optional[int]
    lowest_streak: Optional[int]
    highest_streak: Optional[int]
    games: int
    wins: int
    losses: int
    drops: Optional[int]
    last_match_time: Optional[str]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Leaderboard:
    total: int
    # seems to fall back (?) to 'leaderboard_id' if 'event_leaderboard_id' is not present
    leaderboard_id: Optional[int] = field(metadata=config(field_name="event_leaderboard_id"))
    start: int
    count: int
    players: List[LeaderboardPlayer] = field(metadata=config(field_name="leaderboard"))

    game: str = ""  # defaulting here, will be populated after creation
    # or use 'event_leaderboard_id: Optional[int] = None' and remove 'field' from leaderboard_id
    is_event_leaderboard: bool = False  # defaulting here, will be populated after creation
