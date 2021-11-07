# espn_cfb_api

Python library for accessing the ESPN API for College Football conferences, teams, games, and scores. Currently only FBS conferences are accessible, and only for the current season.

# Classes 
## FBS:
FBS is the highest level class, which contains the hard-coded conferenceIds for the 11 FBS conferences (FBS Independents is treated as a conference by ESPN). 

***Methods***:
```python
getAPTop25Teams(weekNumber = None)
```
Returns a list of Teams( ) as ranked by the AP poll for a given week.
*Note: CFP rankings will be added either as a new method, or a more general method with a ranking type will be developed soon.*
## Conference:
The only argument to initialize the Conference object is the conferenceId as defined by ESPN. Example:
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
...
***README to be updated soon***

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