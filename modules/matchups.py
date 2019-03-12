from modules.models.match import Match
from modules.models.team import Team
from modules.models.completed_match import CompletedMatch
from modules.services.teams_reader import TeamReader

import pandas as pd

input_file = '../data/NCAATourneySeeds.csv'
regular_season_file = '../data/RegularSeasonCompactResults.csv'

class Matchups:
    def __init__(self):
        self.team_reader = TeamReader()
        self.teams_dict = self.team_reader.get_teams()

        
    def get_matchups(self, match_year):
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
                # TODO: We should pass in the day_num as the last parameter
                match = Match(match_year, teamA, teamB, 0)
                matchups.append(match)
        return matchups

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

    def build_teams_dict(self):
        teams[team.id] = team
