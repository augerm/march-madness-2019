from modules.models.kenpom_data import KenPom
class Match:
    def __init__(self, match_year, teamA, teamB, day_num, predicted_result=None):
        self.teamA = teamA
        self.teamB = teamB
        self.year = match_year
        self.day_num = day_num
        self.predicted_result = predicted_result

    def update_result(self, result):
        self.predicted_result = result

    def get_features(self):
        return self.teamA.kenpom_data.get_features() + self.teamB.kenpom_data.get_features()

    @staticmethod
    def get_features_list():
        return KenPom.get_features_list()