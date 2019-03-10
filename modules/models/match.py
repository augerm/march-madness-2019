class Match:
    def __init__(self, theyear, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
        self.year = theyear
        self.predicted_result = None
    
    def update_result(self, result):
        self.predicted_result = result
