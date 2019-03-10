from modules.models.match import Match


class CompletedMatch(Match):

    def __init__(self, match_year, teamA, teamB, day_num, scoreA, scoreB,  predicted_result,result):
        Match.__init__(self, match_year, teamA, teamB, day_num, scoreA, scoreB,  predicted_result)
        self.result = result