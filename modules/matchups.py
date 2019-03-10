from match import Match

import pandas as pd

input_file = 'data/NCAATourneySeeds.csv'
regular_season_file = 'data/RegularSeasonCompactResults.csv'

class Matchups:
    def __init__(self):
        pass
        
    def get_matchups(self):
        theyear = 2018
        data = pd.read_csv(input_file)
        data = data[data['Season']==theyear]
        teamID = list(data['TeamID'].sort_values())
        matchups = []
        for i in range(len(teamID)):
            for j in range(i+1, len(teamID)):
                matchups.append(Match(year = theyear, teamA= teamID[i], teamB=teamID[j]))
        return matchups

    def get_completed_matchups(self):
        data = pd.read_csv(regular_season_file)
        completed_matchups = []
        for i in rang