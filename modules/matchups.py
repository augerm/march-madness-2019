from modules.models.match import Match
from modules.models.team import Team
from modules.models.completed_match import CompletedMatch
from modules.services.teams_reader import TeamReader

import pandas as pd
import numpy as np

input_file = '../data/DataFiles/NCAATourneySeeds.csv'
regular_season_file = '../data/DataFiles/RegularSeasonCompactResults.csv'

class Matchups:
    def __init__(self):
        self.team_reader = TeamReader()
        self.teams_dict = self.team_reader.get_teams()

    def get_matchups_to_predict(self, match_year):
        """
        this is the function to get the matchup for prediction
        """
        data = pd.read_csv(input_file)
        data = data[data['Season'] == match_year]
        teamIDs = list(data['TeamID'].sort_values())
        matchups = []

        for i in range(len(teamIDs)):
            for j in range(i+1, len(teamIDs)):
                teamA_key = Team.get_key(match_year, teamIDs[i])
                teamB_key = Team.get_key(match_year, teamIDs[j])
                teamA = self.teams_dict[teamA_key]
                teamB = self.teams_dict[teamB_key]
                # passing a large number for day_num for predicting matchups 
                match = Match(match_year, teamA, teamB, day_num=300)   
                matchups.append(match)
        return matchups


    def get_completed_matchups_fast(self):
        """
        it is returning a list of dictionaries

        :return:
        """
        data = pd.read_csv(regular_season_file)
        data['teamA'] = data[['WTeamID', 'LTeamID']].min(axis = 1)
        data['teamB'] = data[['WTeamID', 'LTeamID']].max(axis = 1)
        data['scoreA'] = np.where(data['teamA'] == data['WTeamID'], data['WScore'], data['LScore'])
        data['scoreB'] = np.where(data['teamB'] == data['WTeamID'], data['WScore'], data['LScore'])
        data['day_num'] = data['DayNum']
        data['year'] = data['Season']
        data['result'] = np.where(data['scoreA'] > data['scoreB'], 1, 0)
        completed_matchups = data[['year','teamA','teamB','scoreA','scoreB','day_num', 'result']].to_dict('records')
        for i in range(len(completed_matchups)):
            teamA_key = Team.get_key(completed_matchups[i]['year'], completed_matchups[i]['teamA'])
            teamB_key = Team.get_key(completed_matchups[i]['year'], completed_matchups[i]['teamB'])
            teamA = self.teams_dict.get(teamA_key, None)
            teamB = self.teams_dict.get(teamB_key, None)
            completed_matchups[i]['teamA'] = self.teams_dict[teamA_key]
            completed_matchups[i]['teamB'] = self.teams_dict[teamB_key]
            if teamA is None or teamB is None:
                print(i, teamA_key, teamB_key)
            else:
                teamA.add_completed_match(completed_matchups[i])
                teamB.add_completed_match(completed_matchups[i])
        return completed_matchups

    def get_completed_matchups(self):
        data = pd.read_csv(regular_season_file)
        completed_matchups = []
        for i in range(len(data)):
            line = data.loc[i]
            if line['WTeamID'] < line['LTeamID']:
                teamA_key = Team.get_key(line['Season'], line['WTeamID'])
                teamB_key = Team.get_key(line['Season'], line['LTeamID'])
                teamA = self.teams_dict.get(teamA_key, None)
                teamB = self.teams_dict.get(teamB_key, None)
                if not teamA or not teamB:
                    continue
                completed_match = CompletedMatch(line['Season'], teamA, teamB, 0, line['WScore'], line['LScore'], 1)
            else:
                teamA_key = Team.get_key(line['Season'], line['LTeamID'])
                teamB_key = Team.get_key(line['Season'], line['WTeamID'])
                teamA = self.teams_dict.get(teamA_key, None)
                teamB = self.teams_dict.get(teamB_key, None)
                if not teamA or not teamB:
                    continue
                completed_match = CompletedMatch(line['Season'], teamA, teamB, 0, line['WScore'], line['LScore'], 0)
            completed_matchups.append(completed_match)
            teamA.add_completed_match(completed_match)
            teamB.add_completed_match(completed_match)
        return completed_matchups

    # def build_teams_dict(self):
        # teams[team.id] = team
