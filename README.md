# aoe2net-api-wrapper
 A simple and basic Python 3 https://aoe2.net/ API wrapper for sending `GET requests`.
 
 ![GitHub release (latest by date)](https://img.shields.io/github/v/release/sixp-naraka/aoe2net-api-wrapper?color=g&label=GitHub%20release) ![PyPI](https://img.shields.io/pypi/v/aoe2netapi-wrapper?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dd/aoe2netapi-wrapper?label=pypi%20downloads) [![Downloads](https://pepy.tech/badge/aoe2netapi-wrapper)](https://pepy.tech/project/aoe2netapi-wrapper) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aoe2netapi-wrapper)
 
 See the documentation of the API wrapper here on GitHub: [section 'Documentation'](https://github.com/sixP-NaraKa/aoe2net-api-wrapper#documentation).
 
 See https://aoe2.net/#api and https://aoe2.net/#nightbot for the aoe2.net API (documentation) directly.
 
 
 Requirements:
 
 - `requests` >= 2.20.0
 - `dataclasses-json`>=0.5.7
 - Python 3.7+ required
 
 Installation
 -
 Available [on PyPi](https://pypi.org/project/aoe2netapi-wrapper/)
 
 ```
 pip install aoe2netapi-wrapper
 ```
 
 Example usage
 -

 `v1.0.0` and onwards (see issue [#1](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/issues/1) and the [changelog](https://github.com/sixP-NaraKa/aoe2net-api-wrapper#changelog)) there are two different ways, which lead to the same outcome:

 ```python
from aoe2netapi import API, Nightbot, LeaderboardId
from aoe2netapi.constants import LeaderboardId, EventLeaderboardId, Game

api = API()
leaderboard = api.get_leaderboard(leaderboard_id=LeaderboardId.AOE_TWO_RM, search="TheViper")
print(leaderboard)

nightbot = Nightbot()
rank_details = nightbot.get_rank_details(search="TheViper", leaderboard_id=3)
print(rank_details)

# or simply via 'chaining', like this
# leaderboard = API().get_leaderboard(leaderboard_id=3, search="TheViper")

# ...
 ```
 
 Documentation
 -
 See the documentation on the provided functions here on GitHub: [documentation page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/docs.md).
 
 For the documentation for previous versions, see the documentation page here: [documentation page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/).

 Changelog
 -
 See the changelog here on GitHub: [changelog page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/changelog.md).
 
 License
 -
 MIT License. See [LICENSE](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/LICENSE).

