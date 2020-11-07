"""
A simple and basic https://aoe2.net/ api wrapper for sending `GET requests`.

Covers 99% of the aoe2.net API.

Additional data manipulation/extraction from the provided data by this api wrapper has to be done by you, the user.

See https://aoe2.net/#api & https://aoe2.net/#nightbot.
"""


import requests
import logging
import json as jsn


# start and set the logger (in this case as soon as this module has been imported)
logger = logging.getLogger(__name__)


# api base urls
API_BASE = "https://aoe2.net/api"
NIGHTBOT_BASE = API_BASE + "/nightbot"  # "https://aoe2.net/api/nightbot"

# request api base urls (api endpoints)
AB_STRINGS = API_BASE + "/strings"
AB_LEADERBOARD = API_BASE + "/leaderboard"
AB_LOBBIES = API_BASE + "/lobbies"
AB_LAST_MATCH = API_BASE + "/player/lastmatch"
AB_MATCH_HISTORY = API_BASE + "/player/matches"
AB_RATING_HISTORY = API_BASE + "/player/ratinghistory"
AB_MATCHES = API_BASE + "/matches"
AB_MATCH = API_BASE + "/match"
AB_NUMBERS_ONLINE = API_BASE + "/stats/players"

# request nightbot api base urls (api endpoints) -- ? might not be needed (for the api endpoints above you def don't) ;)
NB_RANK_DETAILS = NIGHTBOT_BASE + "/rank?"
NB_RECENT_OPPONENT = NIGHTBOT_BASE + "/opponent?"
NB_CURRENT_MATCH = NIGHTBOT_BASE + "/match?"
NB_CURRENT_CIVS = NIGHTBOT_BASE + "/civs?"
NB_CURRENT_MAP = NIGHTBOT_BASE + "/map?"


# simple base exception class, to raise errors with
class Aoe2NetException(Exception):
    """ AoE2.net API error. """


""" --------------------------------------------- HELPER FUNCTIONS ---------------------------------------------"""


def _is_valid_kwarg(provided: dict, available: dict):
    """
    Helper function to check if a user provided dictionary has the correct arguments,
    compared to a dictionary with the actual available arguments.

    Updates, if no difference found, the dictionary 'available'.

    We don't need to return the updated dictionary since we are calling the dict by reference,
    i.e. the original dict will be changed. ("call by reference", and not "pass by value")
    https://medium.com/@meghamohan/mutable-and-immutable-side-of-python-c2145cf72747

    Parameters
    ----------
    provided : `dict`
        The user defined dictionary of optional additional arguments.
    available : `dict`
        The available optional additional arguments possible.

    :raises KeyError:
        invalid additional keyword argument supplied
    """

    diff = provided.keys() - available.keys()
    if diff:  # if there are differences
        msg = f"invalid optional keyword argument passed: {diff}"
        logger.debug("KeyError, ", msg)
        raise KeyError(msg)
    available.update(provided)


def _get_request_response(link: str, params: dict = None, json: bool = True):
    """
    Helper function to request data.

    For the NIGHTBOT_API calls, the returned data is not JSON, but plain text.
    Each of those functions will return the response.text explicitly.

    Parameters
    ----------
    link : `str`
        The request to call the API with.
    params : `dict`
        A dictionary of parameters that will be used for a GET request.
    json : `bool`
        Specifies if the request response should be returned in JSON format. Defaults to True.

    :return:
        the request response

    :raises requests.exceptions.RequestException:
        if a exception happens during the request handling
    :raises ValueError:
        if status code of the response is not 200
    """

    try:
        response = requests.get(link, params=params)
    except requests.exceptions.RequestException as rer:  # log it and raise 'RequestException'
        logger.exception(rer)
        raise requests.exceptions.RequestException(rer)
    if response.status_code != 200:  # log it and raise 'ValueError'
        msg = f"Expected status code 200 - got {response.status_code}."
        logger.error(msg=msg)
        raise Aoe2NetException(msg)
    if json:
        try:
            response = response.json()
        except jsn.JSONDecodeError as jde:
            logger.error(jde)
            raise Aoe2NetException(jde)
    return response


""" ---------------------------------------- BASE API REQUESTS (ab_...) ----------------------------------------"""


def ab_get_strings(game: str = "aoe2de", json: bool = True):
    """
    Requests a list of strings used by the API.

    Parameters
    ----------
    game : `str`
        The game for which to extract the list of strings. Defaults to "aoe2de" if omitted.

        Possible games:

        aoe2hd -> Age of Empires 2: HD Edition, aoe2de -> Age of Empires 2: Definitive Edition
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    return _get_request_response(link=AB_STRINGS, params={"game": game}, json=json)


def ab_get_leaderboard(leaderboard_id: int = 3, start: int = 1, count: int = 10, json: bool = True, **kwargs):
    """
    Requests the data of the given leaderboard, specified by the 'leaderboard_id'.

    Parameters
    ----------
    leaderboard_id : `int`
        The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

        Possible IDs:

        0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map
    start : `int`
        Specifies the start point for which to extract data at. Defaults to 1.

        Ignored if 'search', 'steam_id' or 'profile_id' are defined.
    count : `int`
        Specifies how many entries of the given ab_leaderboard should be extracted,
        if able to find with the given criteria. Defaults to 10.
        Max. 10000.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        search : `str`
            Specifies a player name to search for. All players found that match the given name will be returned.

        steam_id : `str`
            The steamID64 of a player. (ex: 76561199003184910)

            Takes precedence over both 'search' and 'profile_id'.

        profile_id : `str`
            The profile ID. (ex: 459658)

            Takes precedence over 'search'.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    optionals = {
                "search": "",
                "steam_id": "",
                "profile_id": "",
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"game": "aoe2de", "leaderboard_id": leaderboard_id, "start": start, "count": count}
    params.update(optionals)

    return _get_request_response(link=AB_LEADERBOARD, params=params, json=json)


def ab_get_open_lobbies(game: str = "aoe2de", json: bool = True):
    """
    Requests all open ab_lobbies.

    Parameters
    ----------
    game : `str`
        The game for which to extract the lobby data. Defaults to "aoe2de" if omitted.

        Possible games:

        aoe2hd -> Age of Empires 2: HD Edition, aoe2de -> Age of Empires 2: Definitive Edition
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    params = {"game": game}
    return _get_request_response(link=AB_LOBBIES, params=params, json=json)


def ab_get_last_match(steam_id: str = "", profile_id: str = "", json: bool = True):
    """
    Requests the last match a player started playing.
    This will be the current match if they still are in game.

    Either 'steam_id' or 'profile_id' required.

    Parameters
    ----------
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'profile_id'.
    profile_id : `str`
            The profile ID. (ex: 459658)

            Defaults to an empty string.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    if not steam_id and not profile_id:
        raise ValueError("Either 'steam_id' or 'profile_id' required.")

    params = {"steam_id": steam_id, "profile_id": profile_id}
    return _get_request_response(link=AB_LAST_MATCH, params=params, json=json)


def ab_get_match_history(start: int = 0, count: int = 5, steam_id: str = "", profile_id: str = "", json: bool = True):
    """
    Requests the match history for a player.

    Either 'steam_id' or 'profile_id' required.

    Parameters
    ---------
    start : `int`
        Specifies the start point for which to extract data at. Defaults to 0 (most recent match).
    count : `int`
        Specifies how many entries of the given leaderboard should be extracted,
        if able to find with the given criteria. Defaults to 5.
        Max. 1000.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Defaults to an empty string.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    if not steam_id and not profile_id:
        raise ValueError("Either 'steam_id' or 'profile_id' required.")

    params = {"start": start, "count": count, "steam_id": steam_id, "profile_id": profile_id}
    return _get_request_response(link=AB_MATCH_HISTORY, params=params, json=json)


def ab_get_rating_history(leaderboard_id: int = 3, start: int = 0, count: int = 100, steam_id: str = "", profile_id: str = "", json: bool = True):
    """
    Requests the rating history for a player.

    Either 'steam_id' or 'profile_id' required.

    Parameters
    ---------
    leaderboard_id : `int`
        The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

        Possible IDs:

        0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map
    start : `int`
        Specifies the start point for which to extract data at. Defaults to 0 (most recent match).

        Ignored if 'steam_id' or 'profile_id' are defined.
    count : `int`
        Specifies how many entries of the given leaderboard should be extracted,
        if able to find with the given criteria. Defaults to 100.
        Max. 10000.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Defaults to an empty string.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    if not steam_id and not profile_id:
        raise ValueError("Either 'steam_id' or 'profile_id' required.")

    params = {"leaderboard_id": leaderboard_id, "start": start, "count": count, "steam_id": steam_id, "profile_id": profile_id}
    return _get_request_response(link=AB_RATING_HISTORY, params=params, json=json)


def ab_get_matches(count: int = 5, json: bool = True, **kwargs):
    """
    Requests the match history in a optionally given time frame (globally).

    If 'since' is not set, only the X amount of current past matches (specified by 'count') will be returned.

    Parameters
    ---------
    count : `int`
        Specifies how many entries of the match history should be extracted. Defaults to 5.
        Max. 1000.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        since : `str` | `int`
            Only shows matches after this timestamp. (ex: 1596775000)

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    optionals = {"since": ""}
    _is_valid_kwarg(kwargs, optionals)

    params = {"count": count}
    params.update(optionals)
    return _get_request_response(link=AB_MATCHES, params=params, json=json)


def ab_get_match(uuid: str = "", match_id: str = "", json: bool = True):
    """
    Requests a single match (globally).

    Either 'uuid' or 'match_id' required.

    Parameters
    ---------
    uuid : `str`
        the Match UUID, viewable via a function such as 'ab_get_matches()'.

        Takes precedence over 'match_id'.
    match_id : `str`
        the Match ID, viewable via a function such as 'ab_get_matches()'.
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    if not uuid and not match_id:
        raise ValueError("Either 'uuid' or 'match_id' required.")

    params = {"uuid": uuid, "match_id": match_id}
    return _get_request_response(link=AB_MATCH, params=params, json=json)


def ab_get_num_online(json: bool = True):
    """
    Requests the current player numbers of AoE2: DE.

    Parameters
    ---------
    json : `bool`
        Specifies to the '_get_request_response()' function if the request response should be returned in JSON format.
        Defaults to True.

    :return:
        the data in json format (if set), otherwise the plain response object.
    """

    return _get_request_response(link=AB_NUMBERS_ONLINE, json=json)


""" ---------------------------------------- NIGHTBOT API CALLS (nb_...) ----------------------------------------"""


def nb_get_rank_details(search: str = "", steam_id: str = "", profile_id: str = "", **kwargs):
    """
    Requests the rank details of a player, specified by the 'leaderboard_id'.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found with the given criteria.
    With some combinations of 'search', 'steam_id' and 'profile_id', if nothing could be found for example,
    the current rank #1 player of the given optional additional 'leaderboard_id' will be returned by the API.

    Parameters
    ----------
    search : `str`
        The name of the to be searched player. Returns the highest rated player found.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'search' and 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Takes precedence over 'search'.

        Defaults to an empty string.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        leaderboard_id : `str`
            The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

            Possible IDs:

            0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map

    :return:
        the response.text
    """

    if not search and not steam_id and not profile_id:
        raise ValueError("Either 'search', 'steam_id' or 'profile_id' required.")

    optionals = {
                "leaderboard_id": 3,
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"flag": "false", "search": search.replace(" ", "+"), "steam_id": steam_id, "profile_id": profile_id}
    params.update(optionals)

    return _get_request_response(link=NB_RANK_DETAILS, params=params, json=False).text


def nb_get_recent_opp(search: str = "", steam_id: str = "", profile_id: str = "", **kwargs):
    """
    Requests the rank details of the most recent opponent of a player (1v1 only).

    Either 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.

    Parameters
    ----------
    search : `str`
        The name of the to be searched player. Returns the highest rated player found.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'search' and 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Takes precedence over 'search'.

        Defaults to an empty string.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        leaderboard_id : `str`
            The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

            Is used when 'search' is defined.

            Possible IDs:

            0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map

    :return:
        the response.text
    """

    if not search and not steam_id and not profile_id:
        raise ValueError("Either 'search', 'steam_id' or 'profile_id' required.")

    optionals = {
                "leaderboard_id": 3,
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"flag": "false", "search": search.replace(" ", "+"), "steam_id": steam_id, "profile_id": profile_id}
    params.update(optionals)

    return _get_request_response(link=NB_RECENT_OPPONENT, params=params, json=False).text


def nb_get_current_match(search: str = "", steam_id: str = "", profile_id: str = "", **kwargs):
    """
    Requests details about the last match, or current match if still in game, of a player.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.

    Parameters
    ----------
    search : `str`
        The name of the to be searched player. Returns the highest rated player found.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'search' and 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Takes precedence over 'search'.

        Defaults to an empty string.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        leaderboard_id : `str`
            The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

            Is used when 'search' is defined.

            Possible IDs:

            0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map

        color : `bool`
            The color the players picked in game to play as. Defaults to False.

    :return:
        the response.text
    """

    if not search and not steam_id and not profile_id:
        raise ValueError("Either 'search', 'steam_id' or 'profile_id' required.")

    optionals = {
                "leaderboard_id": 3,
                "color": False
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"flag": "false", "search": search.replace(" ", "+"), "steam_id": steam_id, "profile_id": profile_id}
    params.update(optionals)
    color = params.get("color").__str__().lower()
    params["color"] = color

    return _get_request_response(link=NB_CURRENT_MATCH, params=params, json=False).text


def nb_get_current_civs(search: str = "", steam_id: str = "", profile_id: str = "", **kwargs):
    """
    Requests details about the civilisations from the current (if still in game) or last match.

    Either 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.

    Parameters
    ----------
    search : `str`
        The name of the to be searched player. Returns the highest rated player found.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'search' and 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Takes precedence over 'search'.

        Defaults to an empty string.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        leaderboard_id : `str`
            The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

            Is used when 'search' is defined.

            Possible IDs:

            0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map

    :return:
        the response.text
    """

    if not search and not steam_id and not profile_id:
        raise ValueError("Either 'search', 'steam_id' or 'profile_id' required.")

    optionals = {
                "leaderboard_id": 3
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"search": search.replace(" ", "+"), "steam_id": steam_id, "profile_id": profile_id}
    params.update(optionals)

    return _get_request_response(link=NB_CURRENT_CIVS, params=params, json=False).text


def nb_get_current_map(search: str = "", steam_id: str = "", profile_id: str = "", **kwargs):
    """
    Requests the current map name of a player.

    Either 'search', 'steam_id' or 'profile_id' required.

    The request response is only available as pure text.

    Returns "Player not found", if no player could be found.

    Parameters
    ----------
    search : `str`
        The name of the to be searched player. Returns the highest rated player found.
    steam_id : `str`
        The steamID64 of a player. (ex: 76561199003184910)

        Takes precedence over 'search' and 'profile_id'.
    profile_id : `str`
        The profile ID. (ex: 459658)

        Takes precedence over 'search'.

        Defaults to an empty string.
    **kwargs : `dict`
        Additional optional arguments.

        Possible arguments:

        leaderboard_id : `str`
            The leaderboard in which to extract data in. Defaults to ID 3 (1v1 RM).

            Is used when 'search' is defined.

            Possible IDs:

            0 -> Unranked, 1 -> 1v1 Deathmatch, 2 -> Team Deathmatch, 3 -> 1v1 Random Map, 4 -> Team Random Map

    :return:
        the response.text
    """

    if not search and not steam_id and not profile_id:
        raise ValueError("Either 'search', 'steam_id' or 'profile_id' required.")

    optionals = {
                "leaderboard_id": 3
                }
    _is_valid_kwarg(kwargs, optionals)

    params = {"search": search.replace(" ", "+"), "steam_id": steam_id, "profile_id": profile_id}
    params.update(optionals)

    return _get_request_response(link=NB_CURRENT_MAP, params=params, json=False).text
