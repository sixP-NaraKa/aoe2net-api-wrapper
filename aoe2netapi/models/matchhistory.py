from dataclasses import dataclass, field
from typing import Optional, Any, List
from uuid import UUID

from dataclasses_json import dataclass_json, Undefined, CatchAll


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MatchHistoryPlayer:
    profile_id: str
    name: str
    clan: Optional[str]
    country: Optional[str]
    slot: Optional[int]
    slot_type: Optional[int]
    rating: Optional[int]
    rating_change: Optional[Any]
    color: Optional[int]
    team: Optional[int]
    civ: Optional[int]
    won: Optional[bool]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MatchHistory:
    """
    The match history.
    Encapsulates all properties for AoE2:DE and AoE4.
    For the other available games, no data could be found via the API during the implementation (19.01.2023) -
    that is why the property 'unknown' (a `dict`) is present, which captures all unknown properties that might come up.
    """

    # shared properties (AoE2:DE and AoE4)
    match_id: str
    version: Optional[str]
    name: str
    num_players: Optional[int]
    num_slots: Optional[int]
    has_password: Optional[bool]
    map_size: Optional[int]
    map_type: Optional[int]
    ranked: Optional[bool]
    event_leaderboard_id: Optional[int]
    rating_type_id: Optional[int]
    server: Optional[str]
    started: Optional[str]
    finished: Optional[str]

    # AoE2:DE-only (?) related properties
    match_uuid: Optional[UUID]
    cheats: Optional[bool]
    full_tech_tree: Optional[bool]
    ending_age: Optional[int]
    game_type: Optional[int]
    lock_speed: Optional[bool]
    lock_teams: Optional[bool]
    pop: Optional[int]
    leaderboard_id: Optional[int]
    resources: Optional[int]
    shared_exploration: Optional[bool]
    speed: Optional[int]
    starting_age: Optional[int]
    team_together: Optional[bool]
    team_positions: Optional[bool]
    treaty_length: Optional[int]
    turbo: Optional[bool]
    victory: Optional[int]
    victory_time: Optional[int]

    # dataclass_json catches all other unknown properties into this dict (mapping)
    unknown: CatchAll

    # shared property
    players: List[MatchHistoryPlayer] = field(default_factory=list)
