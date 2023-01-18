"""
A simple and basic Python 3 https://aoe2.net/ API wrapper for sending `GET requests`.

Available on GitHub (+ documentation): https://github.com/sixP-NaraKa/aoe2net-api-wrapper.

See https://aoe2.net/#api & https://aoe2.net/#nightbot for the API documentation directly.
"""
from typing import Union, Any, Dict, List, Tuple, Optional

import requests

from aoe2netapi.constants import Game, LeaderboardId, EventLeaderboardId
from aoe2netapi.models import Strings, Leaderboard, MatchHistory, RatingHistory

API_BASE_URL = "https://aoe2.net/api"
NIGHTBOT_BASE_URL = API_BASE_URL + "/nightbot"  # "https://aoe2.net/api/nightbot"

# api base urls
STRINGS_URL = API_BASE_URL + "/strings"
LEADERBOARD_URL = API_BASE_URL + "/leaderboard"
MATCH_HISTORY_URL = API_BASE_URL + "/player/matches"
RATING_HISTORY_URL = API_BASE_URL + "/player/ratinghistory"

# nightbot api base urls
RANK_DETAILS_URL = NIGHTBOT_BASE_URL + "/rank?"
CURRENT_MATCH_URL = NIGHTBOT_BASE_URL + "/match?"

# request headers
headers = {"content-type": "application/json;charset=UTF-8", "User-Agent": "aoe2netapi-wrapper 2.0.0"}


# simple base exception class, to raise errors with
class Aoe2NetException(Exception):
    """ AoE2.net API error. """


""" ----------------------------------------------- HELPER FUNCTIONS -----------------------------------------------"""


def _is_valid_kwarg(provided: dict, available: dict) -> Dict:
    """
    Helper function to check if a user provided dictionary has the correct arguments,
    compared to a dictionary with the actual available arguments.

    Updates, if no difference found, the dictionary 'available'.

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
        msg = "invalid optional keyword argument passed: {}. Available arguments: {}".format(diff,
                                                                                             list(available.keys()))
        raise KeyError(msg)
    available.update(provided)
    return available


def _get_request_response(url: str, params: dict = None, is_nightbot: bool = False) -> \
        Union[str, Dict[str, Any], List[Any]]:
    """
    Helper function to request data.

    For the `Nightbot` API calls, the returned data is not JSON, but plain text.
    Each of those functions will return the response text explicitly.

    Parameters
    ----------
    url : `str`
        The request to call the API with.
    params : `dict`
        A dictionary of parameters that will be used for a GET request.
    is_nightbot : `bool`
        Specifies if the request response should be returned as text (for the `Nightbot` API calls). Defaults to False.

    :return:
        the request response either as JSON (dict) or text
    """

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.text if is_nightbot else response.json()


def _check_is_leaderboard(leaderboard_id: Union[LeaderboardId, EventLeaderboardId]) -> Tuple[str, bool]:
    """
    Helper function which checks if the given leaderboard ID is valid.

    Unfortunately 'leaderboard_id' and 'event_leaderboard_id'
    are different IDs needing their own request parameter (see aoe2.net API).

    :param leaderboard_id: the leaderboard in which to extract data in

    :returns: the check results

    :raises Aoe2NetException: the given ID is not valid
    """
    if isinstance(leaderboard_id, LeaderboardId):
        return "leaderboard_id", False
    elif isinstance(leaderboard_id, EventLeaderboardId):
        return "event_leaderboard_id", True
    else:
        raise Aoe2NetException("A valid 'leaderboard_id' is required.")


""" ------------------------------------------- API REQUESTS (class API) -------------------------------------------"""


class API:
    """
    The 'API' class encompasses the https://aoe2.net/#api API functions,
    which return their requested data as user-friendly Python objects.
    """

    def get_strings(self, game: Game) -> Strings:
        """
        Requests a list of strings used by the API.

        Parameters
        ----------
        game : :class:`AoEGame`
            The game for which to extract the list of strings.
            Note: For the time being, `AoE1:DE` and `AoE3:DE` throw a 404 here.

        :return:
            the requested data as :class:`Strings`
        """

        result = _get_request_response(url=STRINGS_URL, params={"game": game.value})
        return Strings.from_dict(result)

    def get_leaderboard(self,
                        leaderboard_id: Union[LeaderboardId, EventLeaderboardId],
                        start: int = 1,
                        count: int = 10,
                        **kwargs) -> Leaderboard:
        """
        Requests the data of the given leaderboard, specified by the 'leaderboard_id'.

        Parameters
        ----------
        leaderboard_id : :class:`AoE2NetLeaderboardId` | :class:`AoE2NetEventLeaderboardId`
            The leaderboard in which to extract data in.
        start : `int`
            Specifies the start point for which to extract data at. Defaults to 1.

            Ignored if 'search', 'steam_id' or 'profile_id' are defined.
        count : `int`
            Specifies how many entries of the given leaderboard should be extracted,
            if able to find with the given criteria. Defaults to 10.
            Max. 10000.
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
            the data as :class:`Leaderboard`

        :raises Aoe2NetException:
            'count' has to be 10000 or less or required parameters are missing
        """

        if not start or not count:
            raise Aoe2NetException("'start' and 'count' required.")

        if count > 10000:
            raise Aoe2NetException("'count' has to be 10000 or less.")

        leaderboard_id_param, is_event_leaderboard = _check_is_leaderboard(leaderboard_id=leaderboard_id)

        optionals = {
            "search": "",
            "steam_id": "",
            "profile_id": "",
        }
        optionals = _is_valid_kwarg(kwargs, optionals)

        params = {"game": leaderboard_id.value.game, leaderboard_id_param: leaderboard_id.value.aoe2net_id,
                  "start": start, "count": count}
        params.update(optionals)

        leaderboard = Leaderboard.from_dict(_get_request_response(url=LEADERBOARD_URL, params=params),
                                            infer_missing=True)  # either infer_missing or specify dataclass defaults
        leaderboard.game = leaderboard_id.value.game
        leaderboard.is_event_leaderboard = is_event_leaderboard
        return leaderboard

    def get_match_history(self, game: Game,
                          start: int = 0,
                          count: int = 5,
                          steam_id: str = "",
                          profile_id: str = "") -> List[MatchHistory]:
        """
        Requests the match history for a player.

        'game' required, as well as either 'steam_id' or 'profile_id'.

        Parameters
        ---------
        game : :class:`AoEGame`
            The game for which to extract the match history.
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

        :return:
            the data as :class:`MatchHistory`

        :raises Aoe2NetException:
            'count' has to be 1000 or less || Either 'steam_id' or 'profile_id' required || 'game' is not valid
        """

        if game not in Game:
            raise Aoe2NetException("A valid 'game' is required.")

        if count > 1000:
            raise Aoe2NetException("'count' has to be 1000 or less.")

        if not steam_id and not profile_id:
            raise Aoe2NetException("Either 'steam_id' or 'profile_id' required.")

        params = {"game": game.value, "start": start, "count": count, "steam_id": steam_id, "profile_id": profile_id}
        return [MatchHistory.from_dict(match, infer_missing=True) for match in
                _get_request_response(url=MATCH_HISTORY_URL, params=params)]

    def get_rating_history(self,
                           leaderboard_id: Union[LeaderboardId, EventLeaderboardId],
                           start: int = 0,
                           count: int = 100,
                           steam_id: str = "",
                           profile_id: str = "") -> RatingHistory:
        """
        Requests the rating history for a player.

        Either 'steam_id' or 'profile_id' required.

        Parameters
        ---------
        leaderboard_id : :class:`AoE2NetLeaderboardId` | :class:`AoE2NetEventLeaderboardId`
            The leaderboard in which to extract data in.
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

        :return:
            the data as :class:`RatingHistory`

        :raises Aoe2NetException:
            'count' has to be 10000 or less || Either 'steam_id' or 'profile_id' required
        """

        if count > 10000:
            raise Aoe2NetException("'count' has to be 10000 or less.")

        if not steam_id and not profile_id:
            raise Aoe2NetException("Either 'steam_id' or 'profile_id' required.")

        leaderboard_id_param, is_event_leaderboard = _check_is_leaderboard(leaderboard_id=leaderboard_id)

        params = {"game": leaderboard_id.value.game, leaderboard_id_param: leaderboard_id.value.aoe2net_id,
                  "start": start, "count": count, "steam_id": steam_id, "profile_id": profile_id}
        return RatingHistory(leaderboard_id=leaderboard_id,
                             is_event_leaderboard=is_event_leaderboard,
                             ratings=_get_request_response(url=RATING_HISTORY_URL, params=params))


""" ------------------------------------ NIGHTBOT API REQUESTS (class Nightbot) ------------------------------------"""


class Nightbot:
    """
    The 'Nightbot' class encompasses the https://aoe2.net/#nightbot Nightbot API functions,
    which only return their requested data as plain text.
    """

    def get_rank_details(self, leaderboard_id: Union[LeaderboardId, EventLeaderboardId],
                         search: str = "", steam_id: str = "", profile_id: str = "", flag: bool = True) -> str:
        """
        Requests the rank details of a player, specified by the 'leaderboard_id'.

        Either 'search', 'steam_id' or 'profile_id' required.

        The request response is only available as pure text.

        Returns "Player not found", if no player could be found with the given criteria.

        Parameters
        ----------
        leaderboard_id : :class:`AoE2NetLeaderboardId` | :class:`AoE2NetEventLeaderboardId`
            The leaderboard in which to extract data in.
        search : `str`
            The name of the to be searched player. Returns the highest rated player found.
        steam_id : `str`
            The steamID64 of a player. (ex: 76561199003184910)

            Takes precedence over 'search' and 'profile_id'.
        profile_id : `str`
            The profile ID. (ex: 459658)

            Takes precedence over 'search'.

            Defaults to an empty string.
        flag : `bool`
                The flags of the player. Defaults to True.

        :return:
            the response.text

        :raises Aoe2NetException:
            Either 'search', 'steam_id' or 'profile_id' required
        """

        if not search and not steam_id and not profile_id:
            raise Aoe2NetException("Either 'search', 'steam_id' or 'profile_id' required.")

        leaderboard_id_param, _ = _check_is_leaderboard(leaderboard_id=leaderboard_id)

        params = {"flag": flag.__str__().lower(), "language": "en", "search": search, "steam_id": steam_id,
                  "profile_id": profile_id, leaderboard_id_param: leaderboard_id.value.aoe2net_id,
                  "game": leaderboard_id.value.game}

        return _get_request_response(url=RANK_DETAILS_URL, params=params, is_nightbot=True)

    def get_current_or_last_match(self, search: str = "", steam_id: str = "", profile_id: str = "",
                                  game: Optional[Game] = None, **kwargs):
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
        game : :class:`AoEGame`
            The game for which to extract the match details. If 'search' is used, this is required.
        **kwargs : `dict`
            Additional optional arguments.

            Possible arguments:

            color : `bool`
                The color the players picked in game to play as. Defaults to True.
            flag : `bool`
                The flags of the player. Defaults to True.

        :return:
            the response.text

        :raises Aoe2NetException:
            Either 'search', 'steam_id' or 'profile_id' required || 'search' used but without 'game' specified
        """

        if not search and not steam_id and not profile_id:
            raise Aoe2NetException("Either 'search', 'steam_id' or 'profile_id' required.")

        if search and not game:
            raise Aoe2NetException("'game' is required if 'search' is used.")

        optionals = {
            "color": True,
            "flag": True
        }
        optionals = _is_valid_kwarg(kwargs, optionals)

        params = {"search": search, "steam_id": steam_id, "profile_id": profile_id, "civflag": "false",
                  "game": game.value if game else ""}
        params.update(optionals)
        color = params.get("color").__str__().lower()
        flag = params.get("flag").__str__().lower()
        params["color"] = color
        params["flag"] = flag

        return _get_request_response(url=CURRENT_MATCH_URL, params=params, is_nightbot=True)
