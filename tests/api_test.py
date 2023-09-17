import pytest

from aoe2netapi import API, Aoe2NetException
from aoe2netapi.constants import LeaderboardId, EventLeaderboardId, Game

STRINGS_RESPONSE = {'language': 'en',
                    'age': [{'id': 0, 'string': 'Standard'}],
                    'civ': [{'id': 0, 'string': 'Sample Civ'}],
                    'game_type': [{'id': 0, 'string': 'Random Map'}],
                    'leaderboard': [{'id': 0, 'string': 'Unranked'}],
                    'map_size': [{'id': 0, 'string': 'Tiny (2 player)'}],
                    'map_type': [{'id': 0, 'string': 'Dry Arabia'}],
                    'rating_type': [{'id': 0, 'string': 'Unranked'}],
                    'resources': [{'id': 0, 'string': 'Standard'}],
                    'speed': [{'id': 0, 'string': 'Slow'}],
                    'victory': [{'id': 0, 'string': 'Conquest'}],
                    'visibility': [{'id': 0, 'string': 'Normal'}]}

RM_LEADERBOARD_RESPONSE = {'total': 99999, 'leaderboard_id': 3, 'start': 1, 'count': 3, 'leaderboard': [
    {'profile_id': 1, 'rank': 1, 'rating': 9999, 'steam_id': '1111', 'icon': None,
     'name': 'Sample Player 1', 'clan': None, 'country': '1', 'previous_rating': 9990, 'highest_rating': 9999,
     'streak': 1, 'lowest_streak': -1, 'highest_streak': 11, 'games': 11111, 'wins': 11111, 'losses': 0, 'drops': 0,
     'last_match_time': 0},
    {'profile_id': 2, 'rank': 2, 'rating': 9998, 'steam_id': '2222', 'icon': None,
     'name': 'Sample Player 2', 'clan': None, 'country': '1', 'previous_rating': 9990, 'highest_rating': 9998,
     'streak': 1, 'lowest_streak': -1, 'highest_streak': 11, 'games': 11111, 'wins': 11111, 'losses': 0, 'drops': 0,
     'last_match_time': 0}]}
EMPTY_RM_TEAM_LEADERBOARD_RESPONSE = {'total': 88888, 'leaderboard_id': 4, 'start': 1, 'count': 0, 'leaderboard': []}
EMPTY_EVENT_LEADERBOARD_RESPONSE = {'total': 88888, 'event_leaderboard_id': 1, 'start': 1, 'count': 0,
                                    'leaderboard': []}

MATCH_HISTORY_RESPONSE = [
    {'match_id': 'XXXXXXXXX', 'match_uuid': '4ce4b94b-6606-41e7-8b21-33e61793b1af', 'name': 'AUTOMATCH',
     'num_players': 2, 'num_slots': 8, 'cheats': False, 'full_tech_tree': False, 'ending_age': 5, 'game_type': 0,
     'has_password': False, 'lock_speed': True, 'lock_teams': True, 'map_size': 4, 'map_type': 29, 'pop': 200,
     'ranked': True, 'leaderboard_id': 3, 'rating_type_id': 4, 'resources': 1, 'shared_exploration': True, 'speed': 2,
     'starting_age': 2, 'team_together': True, 'team_positions': True, 'treaty_length': 0, 'turbo': False, 'victory': 0,
     'victory_time': 0, 'started': 1, 'finished': 2, 'players': [
        {'profile_id': 1, 'name': 'Sample Player 1', 'clan': None, 'country': None, 'slot': 1, 'slot_type': 1,
         'rating': 1, 'rating_change': None, 'color': 8, 'team': 1, 'civ': 36, 'won': None},
        {'profile_id': 2, 'name': 'Sample Player 2', 'clan': None, 'country': None, 'slot': 2, 'slot_type': 1,
         'rating': 2, 'rating_change': None, 'color': 1, 'team': 2, 'civ': 34, 'won': None}]}]

RATING_HISTORY_RESPONSE = [
    {'rating': 1, 'num_wins': 1, 'num_losses': 0, 'streak': 0, 'drops': 0, 'timestamp': 1},
    {'rating': 2, 'num_wins': 2, 'num_losses': 0, 'streak': 0, 'drops': 0, 'timestamp': 1}]


def test_get_strings_returns_strings(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=STRINGS_RESPONSE
    )
    api = API()
    strings = api.get_strings(Game.AOE_TWO_DE)
    assert strings.language == "en"
    assert len(strings.age) == 1
    assert len(strings.civ) == 1
    assert len(strings.game_type) == 1
    assert len(strings.leaderboard) == 1
    assert len(strings.map_size) == 1
    assert len(strings.map_type) == 1
    assert len(strings.rating_type) == 1
    assert len(strings.resources) == 1
    assert len(strings.speed) == 1
    assert len(strings.victory) == 1
    assert len(strings.visibility) == 1


@pytest.mark.parametrize("start", [None, 0])
def test_get_leaderboard_throws_aoe2net_exception_when_start_is_none_or_nil(start):
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_leaderboard(LeaderboardId.AOE_TWO_RM, start=start)


@pytest.mark.parametrize("count", [None, 0, 10001])
def test_get_leaderboard_throws_aoe2net_exception_when_count_is_null_nil_or_more_than_10000(count):
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_leaderboard(LeaderboardId.AOE_TWO_RM, count=count)


def test_get_leaderboard_returns_leaderboard(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=RM_LEADERBOARD_RESPONSE
    )
    api = API()
    leaderboard = api.get_leaderboard(LeaderboardId.AOE_TWO_RM)
    assert len(leaderboard.players) == 2
    assert leaderboard.is_event_leaderboard is False
    assert leaderboard.leaderboard_id == LeaderboardId.AOE_TWO_RM.value.aoe2net_id
    assert leaderboard.players[0].name == "Sample Player 1"


def test_empty_get_leaderboard_returns_leaderboard(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=EMPTY_RM_TEAM_LEADERBOARD_RESPONSE
    )
    api = API()
    leaderboard = api.get_leaderboard(LeaderboardId.AOE_TWO_RM_TEAM)
    assert len(leaderboard.players) == 0
    assert leaderboard.is_event_leaderboard is False
    assert leaderboard.leaderboard_id == LeaderboardId.AOE_TWO_RM_TEAM.value.aoe2net_id


def test_get_leaderboard_with_event_leaderboard_id_returns_leaderboard(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=EMPTY_EVENT_LEADERBOARD_RESPONSE
    )
    api = API()
    leaderboard = api.get_leaderboard(EventLeaderboardId.AOE_FOUR_SEASON_ONE)
    assert len(leaderboard.players) == 0
    assert leaderboard.is_event_leaderboard is True
    assert leaderboard.leaderboard_id == EventLeaderboardId.AOE_FOUR_SEASON_ONE.value.aoe2net_id


def test_get_match_history_throws_aoe2net_exception_when_game_is_not_valid():
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_match_history(game=None)


def test_get_match_history_throws_aoe2net_exception_when_count_is_more_than_1000():
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_match_history(game=Game.AOE_TWO_DE, count=1001)


def test_get_match_history_throws_aoe2net_exception_when_steam_id_and_profile_id_are_empty():
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_match_history(game=Game.AOE_TWO_DE, steam_id="", profile_id="")


def test_get_match_history_returns_match_history(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=MATCH_HISTORY_RESPONSE
    )
    api = API()
    match_history = api.get_match_history(game=Game.AOE_TWO_DE, steam_id="x", profile_id="x")
    assert len(match_history) == 1
    assert match_history[0].name == "AUTOMATCH"


def test_get_rating_history_throws_aoe2net_exception_when_count_is_more_than_10000():
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_rating_history(LeaderboardId.AOE_TWO_RM, count=10001)


def test_get_rating_history_throws_aoe2net_exception_when_steam_id_and_profile_id_are_empty():
    api = API()
    with pytest.raises(Aoe2NetException):
        api.get_rating_history(LeaderboardId.AOE_TWO_RM, steam_id="", profile_id="")


def test_get_rating_history_returns_rating_history(mocker):
    mocker.patch(
        "aoe2netapi.aoe2._get_request_response",
        return_value=RATING_HISTORY_RESPONSE
    )
    api = API()
    rating_history = api.get_rating_history(LeaderboardId.AOE_TWO_RM, steam_id="x", profile_id="x")
    assert rating_history.leaderboard_id == LeaderboardId.AOE_TWO_RM.value.aoe2net_id
    assert rating_history.is_event_leaderboard is False
    assert len(rating_history.ratings) == 2
