from modules.models.match import Match


class CompletedMatch(Match):

    def __init__(self, match_year, teamA, teamB, result):
        Match.__init__(self, match_year, teamA, teamB)
        self.result = result
