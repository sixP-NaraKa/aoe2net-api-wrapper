# aoe2net-api-wrapper
 A simple and basic https://aoe2.net/ api wrapper for sending `GET requests`.
 
 See https://aoe2.net/#api and https://aoe2.net/#nightbot for the aoe2.net API documentation.
 
 This wrapper solely supports requesting the data from the aoe2.net api.
 Further data manipulation/extraction required from the requested data has to be done by you, the user.
 
 Requirements:
 
 - `requests` >= 2.20.0
 
 The aoe2.net API has two general API endpoints which we can send requests to:
 
 - `/api` -- for general requests, available in JSON format
 - `/api/nightbot` -- made for Twitch.tv bots (simple commands), only available as pure text
 
 This api wrapper provides the requested data for the `/api` endpoint requests in JSON format,
 or as the plain response object if needed.
 
 The `/api/nightbot` endpoints are only available from the API as pure text.
 The wrapper provides them solely as text.
 
 See the documentation on the provided functions here:
