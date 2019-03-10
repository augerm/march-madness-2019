class OutputGenerator:
    def __init__(self):
        self.output_file = "output/output.txt"

    def write_result(self, matches):
        with open(self.output_file, 'w') as f:
            f.write("id,pred\n")
            for match in matches:
                f.write("{}_{}_{},{}".format(match.year, match.teamA, match.teamB, match.result))