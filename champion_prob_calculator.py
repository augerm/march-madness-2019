import pandas as pd
from modules.services.teams_reader import TeamReader
import math

tourney_seeds_file = 'data/MNCAATourneySeeds.csv'
predictions_file = 'output/output.txt'

class Helper():
    def __init__(self):
        prediction_df = pd.read_csv(predictions_file)
        prediction_keys = prediction_df['id']
        prediction_results = prediction_df['pred']
        self.prediction_dict = {}
        for i in range(len(prediction_keys)):
            key = prediction_keys[i]
            self.prediction_dict[key] = float(prediction_results[i])
            swapped_key = self.swap_teams(key)
            self.prediction_dict[swapped_key] = 1 - float(prediction_results[i])

    @staticmethod
    def swap_teams(key):
        date = key[0:4]
        first_team = key[5:9]
        second_team = key[10:14]
        swapped_teams = "{}_{}_{}".format(date, second_team, first_team)
        return swapped_teams

    @staticmethod
    def get_key(winning_team, losing_team, season):
        return "{}_{}_{}".format(season, winning_team, losing_team)

    def get_win_rate(self, teamIDA, teamIDB, season=2019):
        k = self.get_key(teamIDA, teamIDB, season)
        return self.prediction_dict[k]


class Elimination:
    def __init__(self, seed_count, prob_list):
        assert math.log(seed_count, 2) == int(math.log(seed_count, 2))
        assert seed_count == len(prob_list)
        self.prob_list = prob_list  # store the probability of
        self.next_round_num = int(seed_count/2)
        self.next_prob_list = [None] * self.next_round_num
        self.helper = Helper()

    def print_prob_list(self, n=5):
        print(self.prob_list[:n])

    def get_next_round_num(self):
        return self.next_round_num

    # prob_dict structure -[[{teamid:XXX}, {teamid:prob2}], [{team3, prob3}, {team4, prob4], .....] etc.
    def get_next_prob_list(self):
        for i in range(int(len(self.prob_list)/2)):
            oppo_i = i + int(len(self.prob_list)/2)
            if self.prob_list[i] is None:
                self.next_prob_list[i] = self.prob_list[oppo_i]
            elif self.prob_list[oppo_i] is None:
                self.next_prob_list[i] = self.prob_list[i]
            else:
                new_prob = {}
                for teamIDA in self.prob_list[i].keys():
                    for teamIDB in self.prob_list[oppo_i].keys():
                        pre_probA = self.prob_list[i][teamIDA]
                        pre_probB = self.prob_list[oppo_i][teamIDB]
                        if teamIDA in new_prob:
                            new_prob[teamIDA] += self.helper.get_win_rate(teamIDA, teamIDB) * pre_probA * pre_probB
                        else:
                            new_prob[teamIDA] = self.helper.get_win_rate(teamIDA, teamIDB) * pre_probA * pre_probB
                        if teamIDB in new_prob:
                            new_prob[teamIDB] += self.helper.get_win_rate(teamIDB, teamIDA) * pre_probA * pre_probB
                        else:
                            new_prob[teamIDB] = self.helper.get_win_rate(teamIDB, teamIDA) * pre_probA * pre_probB
                self.next_prob_list[i] = new_prob

    def get_next_elimination(self):
        self.get_next_prob_list()
        return Elimination(self.next_round_num, self.next_prob_list)


# need to build the first round
    # prob_dict structure -[[{teamid:XXX}, {teamid:prob2}], [{team3, prob3}, {team4, prob4], .....] etc.
def build_elimination(season = 2019):
    seed_count = 128
    firstround_prob_list = [None] * seed_count
    tourney_seeds_df = pd.read_csv(tourney_seeds_file)
    tourney_seeds = tourney_seeds_df[tourney_seeds_df['Season'] == season].reset_index(drop=True)
    tourney_seeds['Seed'] = [j + 'a' if not (j.endswith("a") or j.endswith("b")) else j for j in tourney_seeds['Seed']]
    seed_order = []
    for post in ['a','b']:
        for j in range(1, 17):
            j_str = format(j, "02")
            for conf in ['W', 'Y', 'X', 'Z']:
                seed_order.append("{}{}{}".format(conf,j_str,post))
    prob_dict = [None] * seed_count
    for j in range(len(seed_order)):
        seed = seed_order[j]
        if len(tourney_seeds[tourney_seeds['Seed']==seed])>0:
            prob_dict[j] ={}
            teamid = tourney_seeds[tourney_seeds['Seed']==seed]['TeamID'].values[0]
            prob_dict[j][teamid] = 1  # default probability if 1
        else:
            prob_dict[j] = None
    elimination = Elimination(seed_count, prob_dict)
    while elimination.get_next_round_num()>0:
        elimination = elimination.get_next_elimination()
    champion_dict = elimination.prob_list[0]
    champion_dict_sorted = sorted(champion_dict.items(), key=lambda kv: kv[1], reverse=True)
    # print(champion_dict_sorted)
    for info in champion_dict_sorted:
        teamid, probability = info
        print("{}:{:.3f}".format(TeamReader.get_team_name_by_id(teamid), probability))


build_elimination()