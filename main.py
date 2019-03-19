from modules.matchups import Matchups
from modules.match_predictor import MatchPredictor
from modules.output_generator import OutputGenerator


def main():
    match_predictor = MatchPredictor()
    output_generator = OutputGenerator()
    matchups = Matchups()
    matches = matchups.get_matchups_to_predict(2019)

    for match in matches:
        result = match_predictor.get_result(match)
        match.update_result(result)

    output_generator.write_results(matches)

main()
