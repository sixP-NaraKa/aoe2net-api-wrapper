from dataclasses import dataclass, field
from typing import List, NamedTuple

from dataclasses_json import dataclass_json, Undefined, config


@dataclass_json
@dataclass
class StringsItem:
    id: int
    value: str = field(metadata=config(field_name="string"))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Strings:
    language: str
    age: List[StringsItem]
    civ: List[StringsItem]
    game_type: List[StringsItem]
    leaderboard: List[StringsItem]
    map_size: List[StringsItem]
    map_type: List[StringsItem]
    rating_type: List[StringsItem]
    resources: List[StringsItem]
    speed: List[StringsItem]
    victory: List[StringsItem]
    visibility: List[StringsItem]
