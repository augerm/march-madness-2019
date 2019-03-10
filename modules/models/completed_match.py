from modules.models.match import Match


class CompletedMatch(Match):

    def __init__(self, result):
        Match.__init__(self, theyear, teamA, teamB, dayNum, scoreA, scoreB,  predicted_result)
        self.result = result