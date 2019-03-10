class Match:
    def __init__(self, match_year, teamA, teamB, day_num=None, scoreA=None, scoreB=None,  predicted_result= None):
        self.teamA = teamA
        self.teamB = teamB
        self.year = match_year
        self.day_num = day_num
        self.scoreA = scoreA
        self.scoreB = scoreB
        self.predicted_result = predicted_result

    def update_result(self, result):
        self.predicted_result = result
