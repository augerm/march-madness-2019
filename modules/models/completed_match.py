from modules.models.match import Match


class CompletedMatch(Match):

    def __init__(self, match_year, teamA, teamB, day_num, scoreA, scoreB, result, predicted_result = None):
        Match.__init__(self, match_year, teamA, teamB, day_num, predicted_result)
        self.result = result
        self.scoreA = scoreA
        self.scoreB = scoreB
