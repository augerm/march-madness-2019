from modules.models.match import Match
from modules.models.team import Team
from modules.models.completed_match import CompletedMatch
from modules.services.teams_reader import TeamReader

import pandas as pd
import numpy as np
import os

file_path = os.path.dirname(__file__)
input_file = os.path.join(file_path, '../data/DataFiles/NCAATourneySeeds.csv')
regular_season_file = os.path.join(file_path, '../data/DataFiles/RegularSeasonCompactResults.csv')
post_season_file = os.path.join(file_path, '../data/DataFiles/NCAATourneyCompactResults.csv')

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


    def get_completed_matchups(self, until_year=2018):
        """
        until_year: if equal 2018, it will return all regular season of 2018, and regular + post season before 2018

        return a list of completed matchups
        :return:
        """
        def read_compact_result_to_dict(file, last_year, first_year = 2002):
            data = pd.read_csv(file)
            data = data[(data['Season'] <= last_year) & (data['Season'] >= first_year)]
            data['teamA'] = data[['WTeamID', 'LTeamID']].min(axis=1)
            data['teamB'] = data[['WTeamID', 'LTeamID']].max(axis=1)
            data['scoreA'] = np.where(data['teamA'] == data['WTeamID'], data['WScore'], data['LScore'])
            data['scoreB'] = np.where(data['teamB'] == data['WTeamID'], data['WScore'], data['LScore'])
            data['day_num'] = data['DayNum']
            data['year'] = data['Season']
            data['result'] = np.where(data['scoreA'] > data['scoreB'], 1, 0)
            return_dict = data[
                ['year', 'teamA', 'teamB', 'scoreA', 'scoreB', 'day_num', 'result']].to_dict('records')
            return return_dict
        completed_matchups_list_dict = []
        data = read_compact_result_to_dict(regular_season_file,  last_year=until_year)
        post_data = read_compact_result_to_dict(post_season_file, last_year=until_year - 1)
        completed_matchups_list_dict.extend(data)
        completed_matchups_list_dict.extend(post_data)
        completed_matchups = []
        count = 0
        for i in range(len(completed_matchups_list_dict)):
            cur_matchup = completed_matchups_list_dict[i]
            teamA_key = Team.get_key(cur_matchup['year'], cur_matchup['teamA'])
            teamB_key = Team.get_key(cur_matchup['year'], cur_matchup['teamB'])
            # TODO: Remove when we fill out all the non-mapped teams
            if not teamA_key or not teamB_key:
                continue
            teamA = self.teams_dict.get(teamA_key, None)
            teamB = self.teams_dict.get(teamB_key, None)
            completed_match = CompletedMatch(cur_matchup['year'], teamA, teamB,  cur_matchup['day_num'],
                                             cur_matchup['scoreA'], cur_matchup['scoreB'],
                                             cur_matchup['result'])

            if teamA is None or teamB is None:
                count = count + 1
                pass
            else:
                teamA.add_completed_match(completed_match)
                teamB.add_completed_match(completed_match)
                completed_matchups.append(completed_match)
        print("{} of {} games are not added due to missing data.".format(count, len(completed_matchups_list_dict)))
        return completed_matchups


