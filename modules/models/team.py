class Team:
    def __init__(self, year, team_id):
        self.year = year
        self.team_id = team_id
        self.total_points = 0
        self.num_games = 0
        self.id = "{}_{}".format(year, team_id)
        self.ppg = self.total_points / self.num_games

    def add_match(self, match):
        if match.teamA == self.team_id:
            self.total_points += match.scoreA
        elif match.teamB == self.team_id:
            self.total_points += match.scoreB
        else:
            return

        self.num_games += 1
        self.ppg = self.total_points / self.num_games

    @staticmethod
    def get_key(year, team_id):
        return "{}_{}".format(year, team_id)
