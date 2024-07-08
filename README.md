# TODO
- Create a slug when sport or event are created.
- When all the events of a sport are inactive, the sport becomes inactive

- When creating an event the "Logos" property of the event must be populated with logos links related to the teams participating in the event.
Links are available via a third party free API documented here https://www.thesportsdb.com/free_sports_api
The endpoint is:
```www.thesportsdb.com/api/v1/json/3/searchteams.php?t=<QUERY>```
 (Search for team by name) and the relevant key in the response
is ```strLogo.```
**Example:**
event name: "Arsenal vs Leeds";
requests to thesportsdb service:
```GET www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Arsenal```
and
```GET www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Leeds```
format of the stored data in Logos: 
```link_1|link_2```
if one of the links is not found, then use an empty string for the missing link:
```""|link_2``` or ```link_1|"" ```.
If no link is found at all, then store the null value.
**You can assume that a successful response is always correct, so if there are multiple records in the body always refer to the first one.
If, for any reason, the system is unable to get a successful response, the failure must be logged (optionally with a reason).**

