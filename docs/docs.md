# Documentation

 This documentation page comprises v2.0.0+. For the documentation of the previous versions see the [documentation page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs).

 The aoe2.net API has two general API endpoints which we can send requests to:
 
 - `/api` -- for general requests, available in JSON format
 - `/api/nightbot` -- made for Twitch.tv bots (simple commands), only available as pure text
 
 This api wrapper provides the requested data for the `/api` endpoint requests in mapped Python objects (dataclasses).
 
 The `/api/nightbot` endpoints are only available from the API as pure text.
 The wrapper provides them solely as text.
 
 
 `/api` functions (`class API`)
 -
 
 All the applicable functions which use `**kwargs` `raise KeyError` if the optional additional arguments supplied don't exist.
 
 - `get_strings(game) -> Game`
 
    Returns a list of strings used by the API.
 
    Parameters:
    - `game` (Game) -- The game to request for.
    
    Example:
    ````python
    from aoe2netapi import API
    from aoe2netapi.constants import Game
     
    api = API()
    strings = api.get_strings(game=Game.AOE_TWO_DE)
    print(strings)
    # Strings<language="en", age=[StringsItem(id=0, value="Standard"), ...], ...>
    ````
 
 - `get_leaderboard(leaderboard_id, start, count, **kwargs) -> Leaderboard`
 
    Requests the data (players) of the given leaderboard, specified by the 'leaderboard_id'.
 
    Parameters:
    - `leaderboard_id` (LeaderboardId | EventLeaderboardId) -- The leaderboard in which to extract data in.
    - `start` (int) -- Specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'search', 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- Specifies how many entries starting at `start` should be extracted. Defaults to 10.
    - `**kwargs` -- Additional optional arguments.
    
        - `search` (str) -- Specifies a player name to search for. All players found that match the given name will be returned.
        - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
        Takes precedence over both 'search' and 'profile_id'.
        - `profile_id` (str) -- The profile ID. (ex: 459658) Takes precedence over 'search'.
        
    Raises:
    - `Aoe2NetException` - if `count` is more than 10000 or required parameters are missing
        
    Example:
    
    ````python
    from aoe2netapi import API
    from aoe2netapi.models import Leaderboard
    from aoe2netapi.constants import LeaderboardId, EventLeaderboardId
         
    api = API()
    leaderboard: Leaderboard = api.get_leaderboard(leaderboard_id=LeaderboardId.AOE_TWO_RM, count=100)
    print(leaderboard)
    # Leaderboard<total = 43055, leaderboard_id = 3, start = 1, count = 100, players = [...],
    #             game="aoe2de", is_event_leaderboard=False>
   
    for player in leaderboard.players:  # player is of type 'LeaderboardPlayer'
       print(player.rank, player.name, player.rating, player.highest_rating, ...)
    ````

 - `get_match_history(game, start, count, steam_id, profile_id) -> List[MatchHistory]`
 
    Requests the match history for a player.

    'game' required, as well as either 'steam_id' or 'profile_id'.
    
    ##### Note:
    Encapsulates all properties for AoE2:DE and AoE4. For the other available games, no data could be found via the API during the implementation (19.01.2023) - 
    that is why the property 'unknown' (a `dict`) is present, which captures all unknown properties that might come up.
 
    Parameters:
    - `game` (Game) -- The game to request for.
    - `start` (int) -- Specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- Specifies how many entries starting at `start` should be extracted. Defaults to 5.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
    Takes precedence over 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658)
    
    Raises:
    - `Aoe2NetException` - if `count` is more than 1000 || 'game' required, as well as either 'steam_id' or 'profile_id'.
    
    Example:
    ````python
    from typing import List
   
    from aoe2netapi import API
    from aoe2netapi.models import MatchHistory
    from aoe2netapi.constants import Game
     
    api = API()
    match_history: List[MatchHistory] = api.get_match_history(game=Game.AOE_TWO_DE, profile_id="459658")
    print(match_history)
   
    for match in match_history:
       ...
    ````
 
 - `get_rating_history(leaderboard_id, start, count, steam_id, profile_id) -> RatingHistory`
 
    Requests the rating history for a player.

    Either 'steam_id' or 'profile_id' required.
 
    Parameters:
    - `leaderboard_id` (LeaderboardId | EventLeaderboardId) -- The leaderboard in which to extract data in.
    - `start` (int) -- Specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- Specifies how many entries starting at `start` should be extracted. Defaults to 100.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
    Takes precedence over 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658)
    
    Raises:
    - `Aoe2NetException` - if `count` is more than 10000 || Either `steam_id` or `profile_id` required
    
    Example:
    ````python
    from aoe2netapi import API
    from aoe2netapi.models import RatingHistory
    from aoe2netapi.constants import LeaderboardId, EventLeaderboardId
     
    api = API()
    rating_history: RatingHistory = api.get_rating_history(leaderboard_id=LeaderboardId.AOE_TWO_RM, profile_id="459658")
    print(rating_history)
   
    for rating in rating_history.ratings:
       ...
    ````
 
 
 `/api/nightbot` functions (`class Nightbot`)
 -
 
 All the applicable functions which use `**kwargs` `raise KeyError` if the optional additional arguments supplied don't exist.    
 
 - `get_rank_details(leaderboard_id, search, steam_id, profile_id, flag) -> str`
 
    Requests the rank details of a player, specified by the 'leaderboard_id'.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.
    
    Returns "Player not found", if no player could be found.
    
    Parameters:
    - `leaderboard_id` (LeaderboardId | EventLeaderboardId) -- The leaderboard in which to extract data in.
    - `search` (str) -- specifies a player name to search for. Returns the highest rated player found.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
        Takes precedence over both 'search' and 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658) Takes precedence over 'search'.
    - `flag` (bool) -- The flags of the players. Defaults to True.
    
    Raises:
    - `Aoe2NetException` - Either `search`, `steam_id` or `profile_id` required
    
    Example:
    ````python
    from aoe2netapi import Nightbot
    from aoe2netapi.constants import LeaderboardId, EventLeaderboardId
     
    nightbot = Nightbot()
    rank_details: str = nightbot.get_rank_details(leaderboard_id=LeaderboardId.AOE_TWO_RM, search="GL.TheViper")
    print(rank_details)
    # GL.TheViper (2688) Rank #4, has played 1,542 games with a 65% winrate, -1 streak, and 4 drops
    ````
 
 - `get_current_or_last_match(search, steam_id, profile_id, game, **kwargs) -> str`
 
    Requests details about the current or last match of a player.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.
    
    Parameters:
    - `search` (str) -- specifies a player name to search for. Returns the highest rated player found.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
        Takes precedence over both 'search' and 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658) Takes precedence over 'search'.
    - `game` (Game) -- The game for which to extract the match details. If 'search' is used, this is required.
    - `**kwargs` -- Additional optional arguments.
        - `color` (bool) -- The color the players picked in game to play as. Defaults to True.
        - `flag` (bool) -- The flags of the players. Defaults to True.
        
    Raises:
    - `Aoe2NetException` - Either `search`, `steam_id` or `profile_id` required || `search` used but without `game` specified
    
    Example:
    ````python
    from aoe2netapi import Nightbot
    from aoe2netapi.constants import LeaderboardId, EventLeaderboardId
     
    nightbot = Nightbot()
    current_or_last_match: str = nightbot.get_current_or_last_match(leaderboard_id=LeaderboardId.AOE_TWO_RM, search="GL.TheViper")
    print(current_or_last_match)
    ````
    