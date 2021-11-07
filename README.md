# espn_cfb_api

Python library for accessing the ESPN API for College Football conferences, teams, games, and scores. Currently only FBS conferences are accessible, and only for the current season.

# Classes 
## FBS:
FBS is the highest level class, which contains the hard-coded conferenceIds for the 11 FBS conferences (FBS Independents is treated as a conference by ESPN). 

***Methods***:
```python
def getTop25Teams(weekNumber = None, rankingType = 'cfp'):
```
Returns a list of Teams( ) as ranked by the specified poll for a given week.

Available argument for `rankingType` include: 

'ap' [AP Poll]

'cfp' [College Football Playoff] (from Week 10 onwards)

'usa' [Coaches Poll]

## Conference:
The only argument to initialize the Conference object is the `conferenceId` as defined by ESPN. Example:
The SEC is given a conferenceId of 8.
[https://www.espn.com/college-football/conference/_/id/**8**/southeastern-conference](https://www.espn.com/college-football/conference/_/id/8/southeastern-conference)
```python
c = Conference(conferenceId = 8)
print(c.conferenceName)
```
Output:
```
Southeastern Conference
```
***Attributes***:

`conferenceId`, integer designated by ESPN for each FBS conference

`conferenceName`, long-form string of the conference name

*If the conference object is retrieved from a Team object, the divisionId and divisionName are also accessible. Example:*

`divisionId`, integer designated by ESPN for each FBS conference division

`divisionName`, string of the division name

```python
team = Team(teamId = 2)
print(team.displayName)
c = team.getConference()

print(c.conferenceId)
print(c.conferenceName)
print(c.divisionId)
print(c.divisionName)
```

Output:
```
Auburn Tigers
8
Southeastern Conference
7
SEC - West
```


***Methods***:

```python
def getTeams():
```
Returns a list of teams for a given Conference object.

```python
c = Conference(conferenceId = 8)
teams = c.getTeams()
for team in teams:
    print(team.displayName)
```

Output:
```
Georgia Bulldogs
Kentucky Wildcats
Tennessee Volunteers
South Carolina Gamecocks
Florida Gators
Missouri Tigers
Vanderbilt Commodores
Alabama Crimson Tide
Texas A&M Aggies
Ole Miss Rebels
Auburn Tigers
Arkansas Razorbacks
Mississippi State Bulldogs
LSU Tigers
```

```python
def getMatchups(weekNumber = None):
```

Returns a list of Game objects of a given week featuring conference members. Any duplicates should be skipped so only unique Games are returned.

```python
c = Conference(conferenceId = 8)
matchups = c.getMatchups(weekNumber = 10)

for matchup in matchups:
    print(matchup.awayTeam.displayName + ' at ' + matchup.homeTeam.displayName)
```
Output:
```
Missouri Tigers at Georgia Bulldogs
Tennessee Volunteers at Kentucky Wildcats
Florida Gators at South Carolina Gamecocks
LSU Tigers at Alabama Crimson Tide
Auburn Tigers at Texas A&M Aggies
Liberty Flames at Ole Miss Rebels
Mississippi State Bulldogs at Arkansas Razorbacks
```

## Team:
Each team is defined by its `teamId`, as shown on the ESPN url. Example for Auburn (`teamId = 2`):

[https://www.espn.com/college-football/team/_/id/**2**/auburn-tigers](https://www.espn.com/college-football/team/_/id/2/auburn-tigers)

***Attributes***:

`location`, a string of the Team's location, example:  `'Auburn'`

`name`, a string of the Team's name, example:  `'Tigers'`

`displayName`, a combination of location and name, the full team name, example: `'Auburn Tigers'`

`hexcolor`, the hex color of the team's primary color as defined by ESPN. If one doesn't exist, #000000 is used (black)

`record`, a list of integers: [wins, losses]

***Methods***:

```python
def getConference():
```
This returns the associated Conference object of a given team.

```python
def getSchedule(weekNumber = None):
```
If `weekNumber` is defined, a single Game object is returned. 

If no `weekNumber` is defined, a list of all scheduled Games is returned (typically 12 games long).

If a `weekNumber` is requested for a week a Team has no game scheduled, a `NoneType` is returned.

## Game
***Attributes***:

`homeTeam`, the Team object of the home team

`awayTeam`, the Team object of the away team

`weekNumber`, the integer of the week this game took place

***Methods***:

```python
def getWinProbability(key = 'home'):
```

Returns a numpy array of win probability percentage of a given game. By default, the win percentage is with respect to the home team. 

With `key = 'away'` the win probability is with respect to the away team.

#

# Example
Import the library and list the names and record of each team, by FBS division
```python
import espn_cfb_api as cfb

for conference in fbs.getConferences():
    print(conference.conferenceName)
    for team in conference.getTeams():
        print(team.displayName + ' ' + str(team.record))
    print('\n')
```
Output:
```
Atlantic Coast Conference
Wake Forest Demon Deacons [8, 1]
NC State Wolfpack [7, 2]
Clemson Tigers [6, 3]
Syracuse Orange [5, 4]
Boston College Eagles [5, 4]
Louisville Cardinals [4, 5]
Florida State Seminoles [3, 6]
Pittsburgh Panthers [7, 2]
Virginia Cavaliers [6, 3]
Miami Hurricanes [5, 4]
North Carolina Tar Heels [5, 4]
Virginia Tech Hokies [4, 5]
Georgia Tech Yellow Jackets [3, 6]
Duke Blue Devils [3, 6]


American Athletic Conference
Cincinnati Bearcats [9, 0]
Houston Cougars [8, 1]
SMU Mustangs [7, 2]
UCF Knights [6, 3]
East Carolina Pirates [5, 4]
Memphis Tigers [5, 4]
Tulsa Golden Hurricane [3, 6]
Temple Owls [3, 6]
Navy Midshipmen [2, 7]
South Florida Bulls [2, 7]
Tulane Green Wave [1, 8]
...
```