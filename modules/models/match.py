class Match:
    def __init__(self, theyear, teamA, teamB, dayNum=None, scoreA=None, scoreB=None,  predicted_result= None):
        self.teamA = teamA
        self.teamB = teamB
        self.year = theyear
        self.dayNum = dayNum
        self.scoreA = scoreA
        self.scoreB = scoreB
        self.predicted_result = predicted_result

    def update_result(self, result):
        self.predicted_result = result
