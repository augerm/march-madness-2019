from modules.models.match import Match


class CompletedMatch(Match):

<<<<<<< HEAD
    def __init__(self, result):
        Match.__init__(self, theyear, teamA, teamB, dayNum, scoreA, scoreB,  predicted_result)
=======
    def __init__(self, match_year, teamA, teamB, result):
        Match.__init__(self, match_year, teamA, teamB)
>>>>>>> 0285c0b1c4ea259f71bc41c597bba0065776b72d
        self.result = result