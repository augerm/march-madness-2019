from match import Match
import pandas as pd

input_file = 'data/NCAATourneySeeds.csv'

class Matchups:
    def __init__():
        pass
        
    def get_matchups():
        theyear = 2018
        data = pd.read_csv(input_file)
        data = data[data['Season']==theyear]
        teamID = list(data['TeamID'].sort_values())
        matchups = []
        for i in range(len(teamID)):
            for j in range(i+1, len(teamID)):
                matchups.append(Match(year = theyear, teamA= teamID[i], teamB=teamID[j]))
        return matchups