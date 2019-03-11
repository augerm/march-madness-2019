class OutputGenerator:
    def __init__(self):
        self.output_file = "output/output.txt"

    def write_results(self, matches):
        with open(self.output_file, 'w') as f:
            f.write("id,pred\n")
            for match in matches:
                f.write("{}_{}_{},{}\n".format(match.year, match.teamA.team_id, match.teamB.team_id, match.predicted_result))