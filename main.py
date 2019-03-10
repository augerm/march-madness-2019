import matchups
import match_predictor
import output_generator


def main():
    matches = matchups.get_matchups()

    for match in matches:
        result = match_predictor.get_result(match)
        match.update_result(result)

    output_generator.write_results(matches)


main()