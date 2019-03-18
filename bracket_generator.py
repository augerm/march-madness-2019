import pandas
from modules.services.teams_reader import TeamReader

tourney_seeds_file = 'data/Stage2DataFiles/NCAATourneySeeds.csv'
predictions_file = 'output/output.txt'

class BracketGenerator:
    def __init__(self, season):
        self.season = season
        self.tourney_seeds_df = pandas.read_csv(tourney_seeds_file)
        self.predictions = pandas.read_csv(predictions_file)
        self.tourney_seeds = self.tourney_seeds_df[self.tourney_seeds_df['Season'] == self.season]
        confs = ['W', 'X', 'Y', 'Z']
        matchups = {}

        for conf in confs:
            matchups[conf] = []
            matchups[conf] = [j for i,j in zip(self.tourney_seeds['Seed'],self.tourney_seeds['TeamID']) if i.startswith(conf)]
            print(matchups[conf])

        final_four = self.run_bracket_to_final_four(matchups)
        winning_team_w_x = self.get_result(final_four['W'][0], final_four['X'][0])
        winning_team_y_z = self.get_result(final_four['Y'][0], final_four['Z'][0])
        championship_team = self.get_result(winning_team_w_x, winning_team_y_z)

    def run_bracket_to_final_four(self, matchups):
        next_round_matchups = {}
        for conf in matchups.keys():
            next_round_matchups[conf] = []
            # Base case when any conference only has one team
            if (len(matchups[conf]) == 1):
                return matchups
            for i in range(int(len(matchups[conf])/2)):
                teamIDA =  matchups[conf][i]
                teamIDB = matchups[conf][len(matchups[conf])-1-i]
                winning_team_id = self.get_result(teamIDA, teamIDB)
                next_round_matchups[conf].append(winning_team_id)
        return self.run_bracket_to_final_four(next_round_matchups)

    def get_result(self, teamIDA, teamIDB):
        teamA_name = TeamReader.get_team_name_by_id(teamIDA)
        teamB_name = TeamReader.get_team_name_by_id(teamIDB)
        if teamIDA > teamIDB:
            key = "{}_{}_{}".format(self.season, teamIDB, teamIDA)
        else:
            key = "{}_{}_{}".format(self.season, teamIDA, teamIDB)
        result = self.predictions[self.predictions['id'] == key]['pred'].values[0]
        if result >= .5:
            winning_team_id = key[5:9]
        else:
            winning_team_id = key[10:14]
        winning_team = TeamReader.get_team_name_by_id(winning_team_id)
        print("{} vs {} - {}".format(teamA_name, teamB_name, winning_team))
        return winning_team_id



bracket_generator = BracketGenerator(2018)