# Changelog

Changes are listed here. The latest version is currently v1.1.1.

v1.1.1 (07.11.2021)
-

- adjusted documentation (method docstrings + overall documentation under docs/docs.md) to incorporate new 'Empire Wars' game modes (leaderboard IDs)

v1.1.0 (10.04.2021)
-

- helper function `_get_request_response(...)`:
    - moved the request headers `headers = {'content-type': 'application/json;charset=UTF-8'}` outside (in the global scope)
- helper function `_is_valid_kwarg(...)`:
    - now explicitly returning the updated dictionary (just in case)
    - additional error output, specifying which keyword arguments are possible

v1.0.0 (30.12.2020)
-

- moved the API base (`ab_...`) and Nightbot base (`nb_...`) request functions into their respective classes (`API`& `Nightbot`)
    - this changed therefore how the API functions are now called/used
    - a quick example:
    ```python
  import aoe2netapi as aoe
  
  api = aoe.API()
  leaderboard = api.get_leaderboard(leaderboard_id=3, search="TheViper")
  print(leaderboard)

  nightbot = aoe.Nightbot()
  rank_details = nightbot.get_rank_details(search="TheViper", leaderboard_id=3)
  print(rank_details)
  
  # OR like this
  from aoe2netapi import API, Nightbot
  
  api = API()
  leaderboard = api.get_leaderboard(leaderboard_id=3, search="TheViper")
  print(leaderboard)

  nightbot = Nightbot()
  rank_details = nightbot.get_rank_details(search="TheViper", leaderboard_id=3)
  print(rank_details)

    ```

v0.3.0 (24.11.2020)
-

- replaced f-strings with .format() for better backwards-compatibility
- removed the logging for now, might implement it (better) in the future

v0.2.0 (09.11.2020)
-

- Bug fix:
    - ab_get_leaderboard() function - if `search` has been defined with a username that contains whitespaces,
    only the name up to the first whitespace will make it into the URL, and the rest of the criteria will be discarded
        - Fix:
            - replace all whitespaces with "+", for example, via supplying the request headers "headers = {'content-type': 'application/json;charset=UTF-8'}":
             
            "The Viper" > "The+Viper" and the data can now be successfully requested
- the ab_get_num_online() function now also takes in the `game` parameter (either "aoe2de" or "aoe2hd" - "aoe2de" by default)
- removed the `**kwargs` parameter for the nightbot api functions, params (`leaderboard_id`) are now part of the function definition
    - `**kwargs` remains for the nb_get_current_match() function
- for all the functions which use the `count` parameter, 
a condition has been implemented to check for the maximum amount of possible entries at once
- the api functions, if applicable, are now throwing the custom exception `Aoe2NetException`, and not `ValueError` anymore

- noted the above mentioned changes in the general documentation
    - fixed some typos


v0.1.0 (07.11.2020)
-

- initial release