from modules.models.match import Match
from modules.models.team import Team
from modules.models.completed_match import CompletedMatch
import pandas as pd

input_file = 'data/NCAATourneySeeds.csv'
regular_season_file = 'data/RegularSeasonCompactResults.csv'

class Matchups:
    def __init__(self):
        self.teams_dict = {}
        
    def get_matchups(self, match_year):
        data = pd.read_csv(input_file)
        data = data[data['Season'] == match_year]
        teamIDs = list(data['TeamID'].sort_values())
        matchups = []

        for i in range(len(teamIDs)):
            for j in range(i+1, len(teamIDs)):

                teamA_key = Team.get_key(match_year, teamIDs[i])
                if teamA_key in self.teams_dict:
                    teamA = self.teams_dict[teamA_key]
                else:
                    teamA = Team(match_year, teamIDs[i])
                    self.teams_dict[teamA_key] = teamA

                teamB_key = Team.get_key(match_year, teamIDs[j])
                if teamB_key in self.teams_dict:
                    teamB = self.teams_dict[teamB_key]
                else:
                    teamB = Team(match_year, teamIDs[j])
                    self.teams_dict[teamB_key] = teamB

                match = Match(match_year, teamA, teamB, 0)

                matchups.append(match)
        return matchups

    def get_completed_matchups(self):
        data = pd.read_csv(regular_season_file)
        completed_matchups = []
        for i in range(len(data)):
            line = data.loc[i]
            if line['WTeamID'] < line['LTeamID']:
                completed_matchups.append(CompletedMatch(year = line['Season'], teamA = line['WTeamID'], teamB = line['LTeamID'],
                    scoreA = line['WScore'], scoreB = line['LScore'], result = True, day_num = line['DayNum']))
                year = line['Season']
                teamA_id = line['WTeamID']
                teamA_score = line['WScore']
                teamB_id = line['LTeamID']
                teamB_score = line['LScore']
                day_num = line['DayNum']
                teamA_key = Team.get_key(year, teamA_id)
                teamB_key = Team.get_key(year, teamB_id)
                match = Match(year, teamA_id, teamB_id, day_num, teamA_score, teamB_score)
                teamA.add_completed_match(match)
                teamB.add_completed_match(match)


            else:
                completed_matchups.append(CompletedMatch(year = line['Season'], teamB = line['WTeamID'], teamA = line['LTeamID'], 
                    scoreB = line['WScore'], scoreA = line['LScore'], result = False, day_num = line['DayNum']))
                year = line['Season']
                teamA_id = line['LTeamID']
                teamA_score = line['LScore']
                teamB_id = line['WTeamID']
                teamB_score = line['WScore']
                day_num = line['DayNum']
                teamA_key = Team.get_key(year, teamA_id)
                teamB_key = Team.get_key(year, teamB_id)
                match = Match(year, teamA_id, teamB_id, day_num, teamA_score, teamB_score)
                teamA.add_completed_match(match)
                teamB.add_completed_match(match)

        return completed_matchups

    def build_teams_dict(self):
        teams[team.id] = team
