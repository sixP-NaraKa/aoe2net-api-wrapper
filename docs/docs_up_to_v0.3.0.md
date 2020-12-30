# Documentation

 This documentation page comprises v0.3.0. For the documentation of v1.0.0 and onwards, see the [documentation page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/docs.md) here.

 The aoe2.net API has two general API endpoints which we can send requests to:
 
 - `/api` -- for general requests, available in JSON format
 - `/api/nightbot` -- made for Twitch.tv bots (simple commands), only available as pure text
 
 This api wrapper provides the requested data for the `/api` endpoint requests in JSON format,
 or as the plain response object if needed.
 
 The `/api/nightbot` endpoints are only available from the API as pure text.
 The wrapper provides them solely as text.
 
 
 `/api` functions
 -
 
 All the applicable functions which use `**kwargs` `raise KeyError` if the optional additional arguments supplied don't exist.
 
 - `ab_get_strings(game, json)`
 
    Returns a list of strings used by the API.
 
    Parameters:
    - `game` (str) -- The game to request for. "aoe2de" or "aoe2hd" available. Defaults to "aoe2de".
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True
 
 - `ab_get_leaderboard(leaderboard_id, start, count, json, **kwargs)`
 
    Requests the data (players) of the given leaderboard, specified by the 'leaderboard_id'.
 
    Parameters:
    - `leaderboard_id` (int) -- the leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM). 
    0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map
    - `start` (int) -- specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'search', 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- specifies how many entries starting at `start` should be extracted. Defaults to 10.
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    - `**kwargs` -- Additional optional arguments.
    
        - `search` (str) -- specifies a player name to search for. All players found that match the given name will be returned.
        - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
        Takes precedence over both 'search' and 'profile_id'.
        - `profile_id` (str) -- The profile ID. (ex: 459658) Takes precedence over 'search'.
        
    Raises:
    - `Aoe2NetException` - if `count` is more than 10000
        
    Example:
    
```python
import aoe2netapi as aoe
     
result = aoe.ab_get_leaderboard(leaderboard_id=3, count=100, json=True)
print(result)
```
 This will return and print the top 100 players of the 1v1 RM leaderboard in JSON format.
    
    
 - `ab_get_open_lobbies(game, json)`
 
    Requests all open lobbies.
 
    Parameters:
    - `game` (str) -- The game to request for. "aoe2de" or "aoe2hd" available. Defaults to "aoe2de".
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True
 
 - `ab_get_last_match(steam_id, profile_id, json)`
 
    Requests the last match a player started playing.
    This will be the current match if they still are in game.

    Either 'steam_id' or 'profile_id' required.
 
    Parameters:
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
    Takes precedence over 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658)
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    
    Raises:
    - `Aoe2NetException` - Either `steam_id` or `profile_id` required.
 
 - `ab_get_match_history(start, count, steam_id, profile_id, json)`
 
    Requests the match history for a player.

    Either 'steam_id' or 'profile_id' required.
 
    Parameters:
    - `start` (int) -- specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- specifies how many entries starting at `start` should be extracted. Defaults to 5.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
    Takes precedence over 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658)
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    
    Raises:
    - `Aoe2NetException` - if `count` is more than 1000 || Either `steam_id` or `profile_id` required.
 
 - `ab_get_rating_history(leaderboard_id, start, count, steam_id, profile_id, json)`
 
    Requests the rating history for a player.

    Either 'steam_id' or 'profile_id' required.
 
    Parameters:
    - `leaderboard_id` (int) -- the leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM). 
    0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map
    - `start` (int) -- specifies the start point for which to extract data at. Defaults to 1 (first entry).
    Ignored if 'steam_id' or 'profile_id' are defined.
    - `count` (int) -- specifies how many entries starting at `start` should be extracted. Defaults to 100.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
    Takes precedence over 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658)
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    
    Raises:
    - `Aoe2NetException` - if `count` is more than 1000 || Either `steam_id` or `profile_id` required.
 
 - `ab_get_matches(count, json, **kwargs)`
 
    Requests the match history in a optionally given time frame (globally).

    If 'since' is not set, only the X amount of current past matches (specified by 'count') will be returned.
 
    Parameters:
    - `count` (int) -- specifies how many entries starting at `start` should be extracted. Defaults to 5.
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    - `**kwargs` -- Additional optional arguments.
    
        - `since` (str | int) -- only shows matches after this timestamp. (ex: 1596775000)
        
    Raises:
    - `Aoe2NetException` - if `count` is more than 1000
 
 - `ab_get_match(uuid, match_id, json)`
 
    Requests a single match (globally).

    Either 'uuid' or 'match_id' required.
 
    Parameters:
    - `uuid` (str) -- the Match UUID, viewable via a function such as 'ab_get_matches()'. 
    Takes precedence over 'match_id'.
    - `match_id` (str) -- the Match ID, viewable via a function such as 'ab_get_matches()'.
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
    
    Raises:
    - `Aoe2NetException` - Either `uuid` or `match_id` required
 
 - `ab_get_num_online(game, json)`
 
    Requests the current player numbers of AoE2: DE.
 
    Parameters:
    - `game` (str) -- The game to request for. "aoe2de" or "aoe2hd" available. Defaults to "aoe2de".
    - `json` (bool) -- whether the request should be returned in JSON format. If set to False, the response object will be returned. 
    Defaults to True.
 
 
 `/api/nightbot` functions
 -
 
 All the applicable functions which use `**kwargs` `raise KeyError` if the optional additional arguments supplied don't exist.
 
  
 - All the `/api/nightbot` functions use the following parameters and raise the same exception:
 
    - `search` (str) -- specifies a player name to search for. Returns the highest rated player found.
    - `steam_id` (str) -- The steamID64 of a player. (ex: 76561199003184910). 
        Takes precedence over both 'search' and 'profile_id'.
    - `profile_id` (str) -- The profile ID. (ex: 459658) Takes precedence over 'search'.     
    - `leaderboard_id` (int) -- the leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM). 
    0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map
    
    Raises:
    - `Aoe2NetException` - Either `search`, `steam_id` or `profile_id` required.
    
 
 - `nb_get_rank_details(search, steam_id, profile_id, leaderboard_id)`
 
    Requests the rank details of a player, specified by the 'leaderboard_id'.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.
    
 
 - `nb_get_recent_opp(search, steam_id, profile_id, leaderboard_id)`
 
    Requests the rank details of the most recent opponent of a player (1v1 only).

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.
    
 
 - `nb_get_current_match(search, steam_id, profile_id, leaderboard_id, **kwargs)`
 
    Requests details about the last match, or current match if still in game, of a player.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.
    
    Additional Parameter:
    - `color` (bool) -- The color the players picked in game to play as. Defaults to False.
    
 
 - `nb_get_current_civs(search, steam_id, profile_id, leaderboard_id)`
 
    Requests details about the civilisations from the current (if still in game) or last match.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.
    
 
 - `nb_get_current_map(search, steam_id, profile_id, leaderboard_id)`
 
    Requests the current map name of a player.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.
    