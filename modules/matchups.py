from modules.models.match import Match
from modules.models.completed_match import CompletedMatch
import pandas as pd

input_file = 'data/NCAATourneySeeds.csv'
regular_season_file = 'data/RegularSeasonCompactResults.csv'

class Matchups:
    def __init__(self):
        pass
        
    def get_matchups(self):
        match_year = 2018
        data = pd.read_csv(input_file)
        data = data[data['Season']==match_year]
        teamID = list(data['TeamID'].sort_values())
        matchups = []
        for i in range(len(teamID)):
            for j in range(i+1, len(teamID)):
                matchups.append(Match(year = theyear, teamA= teamID[i], teamB=teamID[j]))
        return matchups

    def get_completed_matchups(self):
        data = pd.read_csv(regular_season_file)
        completed_matchups = []
        for i in range(len(data)):
            line = data.loc[i]
            if line['WTeamID'] < line['LTeamID']:
                completed_matchups.append(CompletedMatch(year = line['Season'], teamA = line['WTeamID'], teamB = line['LTeamID'], 
                    scoreA = line['WScore'], scoreB = line['LScore'], result = True, day_num = line['DayNum']))
            else:
                completed_matchups.append(CompletedMatch(year = line['Season'], teamB = line['WTeamID'], teamA = line['LTeamID'], 
                    scoreB = line['WScore'], scoreA = line['LScore'], result = False, day_num = line['DayNum']))
        return completed_matchups
