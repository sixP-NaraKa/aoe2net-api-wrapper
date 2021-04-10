# aoe2net-api-wrapper
 A simple and basic Python 3 https://aoe2.net/ API wrapper for sending `GET requests`.
 
 ![GitHub release (latest by date)](https://img.shields.io/github/v/release/sixp-naraka/aoe2net-api-wrapper?color=g&label=GitHub%20release) ![PyPI](https://img.shields.io/pypi/v/aoe2netapi-wrapper?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dd/aoe2netapi-wrapper?label=pypi%20downloads) [![Downloads](https://pepy.tech/badge/aoe2netapi-wrapper)](https://pepy.tech/project/aoe2netapi-wrapper) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aoe2netapi-wrapper)
 
 See the documentation of the API wrapper here on GitHub: [section 'Documentation'](https://github.com/sixP-NaraKa/aoe2net-api-wrapper#documentation).
 
 See https://aoe2.net/#api and https://aoe2.net/#nightbot for the aoe2.net API (documentation) directly.
 
 This wrapper solely supports requesting the data from the aoe2.net API.
 Further data manipulation/extraction required from the requested data has to be done by you, the user.
 
 Requirements:
 
 - `requests` >= 2.20.0
 - Python 3.X required (3.5+)
 
 Installation
 -
 Available [on PyPi](https://pypi.org/project/aoe2netapi-wrapper/)
 
 ```
 pip install aoe2netapi-wrapper
 ```
 
 Example usage
 -
 up to and including `v0.3.0`:
 
 ```python
import aoe2netapi as aoe

leaderboard = aoe.ab_get_leaderboard(leaderboard_id=3, search="TheViper")
print(leaderboard)

rank_details = aoe.nb_get_rank_details(search="TheViper", leaderboard_id=3)
print(rank_details)

# ...
 ```

 `v1.0.0` and onwards (see issue [#1](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/issues/1) and the [changelog](https://github.com/sixP-NaraKa/aoe2net-api-wrapper#changelog)) there are two different ways, which lead to the same outcome:
 
 1.) importing the usual way
 ```python
import aoe2netapi as aoe

api = aoe.API()
leaderboard = api.get_leaderboard(leaderboard_id=3, search="TheViper")
print(leaderboard)

nightbot = aoe.Nightbot()
rank_details = nightbot.get_rank_details(search="TheViper", leaderboard_id=3)
print(rank_details)

# ...
```

 2.) via their respective classes
 ```python
from aoe2netapi import API, Nightbot

api = API()
leaderboard = api.get_leaderboard(leaderboard_id=3, search="TheViper")
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
 
 For the documentation for up to and including v0.3.0, see the documentation page here: [documentation page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/docs_up_to_v0.3.0.md).

 Changelog
 -
 See the changelog here on GitHub: [changelog page](https://github.com/sixP-NaraKa/aoe2net-api-wrapper/blob/main/docs/changelog.md).


