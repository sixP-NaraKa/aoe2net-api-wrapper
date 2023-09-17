import pytest

from aoe2netapi import Nightbot, Aoe2NetException
from aoe2netapi.constants import LeaderboardId, Game

PLAYER_NOT_FOUND = "Player not found"
RANK_DETAILS = "Sample Player (9999) Rank #1, has played 9,999 games with a 100% winrate, +9999 streak, and 0 drops"
CURRENT_OR_LAST_MATCH = \
    "Sample Player 1 (9999) as Mongols -VS- Sample Player 2 (9998) as English playing on King of Hill"


def test_get_rank_details_throws_aoe2net_exception_when_search_and_steam_id_and_profile_id_are_empty():
    nightbot = Nightbot()
    with pytest.raises(Aoe2NetException):
        nightbot.get_rank_details(LeaderboardId.AOE_TWO_RM)


def test_get_rank_details_returns_player_not_found(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=PLAYER_NOT_FOUND
    )
    nightbot = Nightbot()
    rank_details = nightbot.get_rank_details(LeaderboardId.AOE_TWO_RM, search="Sample Player")
    assert rank_details == PLAYER_NOT_FOUND


def test_get_rank_details_returns_rank_details(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=RANK_DETAILS
    )
    nightbot = Nightbot()
    rank_details = nightbot.get_rank_details(LeaderboardId.AOE_TWO_RM, search="Sample Player")
    assert rank_details == RANK_DETAILS


def test_get_current_or_last_match_throws_aoe2net_exception_when_search_and_steam_id_and_profile_id_are_empty():
    nightbot = Nightbot()
    with pytest.raises(Aoe2NetException):
        nightbot.get_current_or_last_match()


def test_get_current_or_last_match_throws_aoe2net_exception_when_search_requires_game():
    nightbot = Nightbot()
    with pytest.raises(Aoe2NetException):
        nightbot.get_current_or_last_match(search="Sample Player")


def test_get_current_or_last_match_returns_player_not_found(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=PLAYER_NOT_FOUND
    )
    nightbot = Nightbot()
    rank_details = nightbot.get_current_or_last_match(search="Sample Player", game=Game.AOE_TWO_DE)
    assert rank_details == PLAYER_NOT_FOUND


def test_get_current_or_last_match_returns_current_or_last_match(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=CURRENT_OR_LAST_MATCH
    )
    nightbot = Nightbot()
    current_or_last_match = nightbot.get_rank_details(LeaderboardId.AOE_TWO_RM, search="Sample Player")
    assert current_or_last_match == CURRENT_OR_LAST_MATCH
