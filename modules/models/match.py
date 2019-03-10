class Match:
    def __init__(self, match_year, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
        self.year = match_year
        self.predicted_result = None
    
    def update_result(self, result):
        self.predicted_result = result
