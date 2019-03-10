class Match:
    def __init__(self, theyear, teamA, teamB, dayNum=None, scoreA=None, scoreB=None, result=None, predicted_result = None):
        self.teamA = teamA
        self.teamB = teamB
        self.year = theyear
        self.predicted_result = None
        self.dayNum = dayNum
        self.scoreA = scoreA
        self.scoreB = scoreB
        self.result = None  # teamA win - 1, lose - 0
    
    def update_result(self, result):
        self.result = result
