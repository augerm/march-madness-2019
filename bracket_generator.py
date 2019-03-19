import pandas
from modules.services.teams_reader import TeamReader

tourney_seeds_file = 'data/Stage2DataFiles/NCAATourneySeeds.csv'
predictions_file = 'output/output.txt'

class BracketGenerator:
    def __init__(self, season):
        self.season = season
        self.tourney_seeds_df = pandas.read_csv(tourney_seeds_file)
        self.predictions = pandas.read_csv(predictions_file)
        self.tourney_seeds = self.tourney_seeds_df[self.tourney_seeds_df['Season'] == self.season].reset_index(drop=True)
        confs = ['W', 'X', 'Y', 'Z']
        matchups = {}
        self.run_pre_round()

        for conf in confs:
            matchups[conf] = []
            matchups[conf] = [j for i,j in zip(self.tourney_seeds['Seed'],self.tourney_seeds['TeamID']) if i.startswith(conf)]
            # print(matchups[conf])

        final_four = self.run_bracket_to_final_four(matchups)
        winning_team_w_x = self.get_result(final_four['W'][0], final_four['X'][0])
        winning_team_y_z = self.get_result(final_four['Y'][0], final_four['Z'][0])
        championship_team = self.get_result(winning_team_w_x, winning_team_y_z)

    def run_pre_round(self):
        prematchup_teams_a = self.tourney_seeds[self.tourney_seeds['Seed'].str.endswith("a")]
        for seed_a, id in zip(prematchup_teams_a['Seed'].values, prematchup_teams_a['TeamID'].values):
            seed_b = seed_a.replace('a', 'b')
            teamIDB = self.tourney_seeds[self.tourney_seeds['Seed']==seed_b]['TeamID'].values[0]
            # teamB_name = TeamReader.get_team_name_by_id(teamIDA)
            teamIDA = id
            # teamA_name = TeamReader.get_team_name_by_id(teamIDA)
            print("preround - {} - {}".format(seed_a, seed_b))
            new_seed = seed_a[:-1]
            winningteam = int(self.get_result(teamIDA, teamIDB))
            self.tourney_seeds.loc[len(self.tourney_seeds)] = [self.season, new_seed, winningteam]
        self.tourney_seeds = self.tourney_seeds[~self.tourney_seeds['Seed'].str.endswith("a")]
        self.tourney_seeds = self.tourney_seeds[~self.tourney_seeds['Seed'].str.endswith("b")]
        self.tourney_seeds = self.tourney_seeds.sort_values('Seed').reset_index(drop=True)


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
        print("{} vs {} - {} - {:.3f}".format(teamA_name, teamB_name, winning_team, max(result, 1-result)))
        return int(winning_team_id)



bracket_generator = BracketGenerator(2019)