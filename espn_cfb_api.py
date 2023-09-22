import requests
import numpy as np

class FBS:
    def __init__(self):
        self.year = 2023
        
    def getConferences(self):
            
        # All FBS conferenceIds hard-coded for an initial starting pt
        conferenceIds = [1, 151, 5, 4, 12, 18, 15, 17, 9, 8, 37]
        return [Conference(conferenceId) for conferenceId in conferenceIds]
    
    def getTop25Teams(self, weekNumber=None, rankingType = 'ap'):
        Top25TeamsList = list()
        url = f'http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings?seasons={self.year}&weeks={weekNumber}'
        req = requests.get(url)
        data = req.json()
        
        rankings = data['rankings']
        for ranking in rankings:
            if ranking['type'] == rankingType:
                ranks = ranking['ranks']        
                Top25TeamsList = [Team(teamId = int(rank['team']['id'])) for rank in ranks]
                return tuple(Top25TeamsList)
        return None

class Conference:
    def __init__(self, conferenceId=None, divisionId=None):
        self.conferenceId = conferenceId
        self.divisionId = divisionId
        self.conferenceName = ''
        self.divisionName = ''
        self.url = 'https://site.api.espn.com/apis/v2/sports/football/college-football/standings'
        req = requests.get(self.url)
        data = req.json()
        
        for conference in data['children']:
            if str(self.conferenceId) in conference.values():
                self.cdata = conference
                self.conferenceName = conference['name']
                
                if 'children' in conference:
                    for division in conference['children']:
                        if str(self.divisionId) in division.values():
                            self.divisionName = division['name']
    
    def getTeams(self):
        teamList = list()
        if 'children' in self.cdata:
            for division in self.cdata['children']:
                for team in division['standings']['entries']:
                    teamList.append(Team(int(team['team']['id'])))
            return teamList
        else:
            for team in self.cdata['standings']['entries']:
                teamList.append(Team(int(team['team']['id'])))
            return teamList
    
    def getMatchups(self, weekNumber=None):
        matchups = list()
        teams = self.getTeams()
        for team in teams:
            skip = False
            game = team.getSchedule(weekNumber = weekNumber)
            if game is not None:
                if len(matchups) > 0:
                    for matchup in matchups:
                        matchupIds = [matchup.homeTeam.teamId, matchup.awayTeam.teamId]
                        if team.teamId in matchupIds:
                            skip = True
                            
                    if not skip:
                        matchups.append(game)
                else:
                    matchups.append(game)
        return matchups
        
class Team:
    def __init__(self, teamId=None):
        self.teamId = teamId
        self.year = 2023 # hard-coded for now to this season
        self.url = ''
        self.tdata = self.getTeamData()
        
        # Pull team-level data from json
        self.name = self.tdata['name']
        self.location = self.tdata['location']
        self.displayName = self.tdata['displayName']
        self.record = [int(s) for s in self.tdata['recordSummary'].split('-')]
        try:
            self.hexColor = '#'+self.tdata['color']
        except:
            self.hexColor = '#000000'

    def getTeamData(self):
        self.url = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{self.teamId}/schedule?season={self.year}'
        req = requests.get(self.url)
        data = req.json()
        self.sdata = data['events']
        return data['team']
    
    def getConference(self):
        group = self.tdata['groups']
        if group['isConference'] == True:
            self.divisionId = None
            self.divisionName = ''
            self.conferenceId = int(group['id'])
        elif group['isConference'] == False:
            self.divisionId = int(group['id'])
            self.conferenceId = int(group['parent']['id'])
        
        # Generate a Conference object
        c = Conference(conferenceId = self.conferenceId, divisionId = self.divisionId)
        
        return c
    
    def getSchedule(self, weekNumber=None):
        gameList = list()
        for game in self.sdata:
            if not weekNumber:
                gameList.append(Game(gameId = int(game['id'])))
            elif weekNumber is not None:
                if weekNumber == game['week']['number']:
                    gameList = Game(gameId = int(game['id']))
        if isinstance(gameList, list):
            if len(gameList) == 0:
                return None
        return gameList
        
class Game:
    def __init__(self, gameId=None):
        self.gameId = gameId
        self.url = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={self.gameId}'
        req = requests.get(self.url)
        self.gdata = req.json()
        self.homeTeam = Team(teamId = int(self.gdata['header']['competitions'][0]['competitors'][0]['id']))
        self.awayTeam = Team(teamId = int(self.gdata['header']['competitions'][0]['competitors'][1]['id']))
        self.weekNumber = self.gdata['header']['week']
    
    def getWinProbability(self, key = 'home'):
        prob_array = np.array([])
        if 'winprobability' in self.gdata:
            for prob_pt in self.gdata['winprobability']:
                if key == 'home':
                    prob_array = np.append(prob_array, float(prob_pt['homeWinPercentage'])*100)
                elif key == 'away':
                    prob_array = np.append(prob_array, (1 - float(prob_pt['homeWinPercentage']))*100)
        
        return prob_array