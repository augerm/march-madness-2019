class Match:
    def __init__(self, theyear, teamA, teamB, result = None):
        self.teamA = teamA
        self.teamB = teamB
        self.year = theyear
        self.result = None
    
    def update_result(self, result):
        self.result = result
