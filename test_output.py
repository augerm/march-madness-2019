import pandas
from modules.loss_function import get_loss_single
from modules.services.teams_reader import TeamReader

prediction_file = 'output/output.txt'
results_file = 'data/MNCAATourneyCompactResults.csv'

prediction_df = pandas.read_csv(prediction_file)
results_df = pandas.read_csv(results_file)

results_seasons = list(results_df['Season'])
results_winning_team = list(results_df['WTeamID'])
results_losing_team = list(results_df['LTeamID'])


def swap_teams(key):
    date = key[0:4]
    first_team = key[5:9]
    second_team = key[10:14]
    swapped_teams = "{}_{}_{}".format(date, second_team, first_team)
    return swapped_teams

def get_key(winning_team, losing_team, season):
    return "{}_{}_{}".format(season, winning_team, losing_team)

prediction_keys = prediction_df['id']
prediction_results = prediction_df['pred']
prediction_dict = {}

for i in range(len(prediction_keys)):
    key = prediction_keys[i]
    prediction_dict[key] = float(prediction_results[i])
    swapped_key = swap_teams(key)
    prediction_dict[swapped_key] = 1 - float(prediction_results[i])

def get_loss(winning_team, losing_team, season):
    key = get_key(winning_team, losing_team, season)
    predicted_result = prediction_dict.get(key, None)
    if predicted_result is None:
        print("Failed to find matchup: {}".format(key))
        return None
    predicted_team = key[5:9]
    if predicted_result >= .5:
        correct_pick = True
        loss = get_loss_single(predicted_result, 1)
    elif predicted_result < .5:
        correct_pick = False
        loss = get_loss_single(predicted_result, 1)

    return {
        'loss': loss,
        'correct': correct_pick,
        'prediction': predicted_result,
        'predicted_team': predicted_team,
        'winning_team_id': winning_team,
        'losing_team_id': losing_team,
        'winning_team': TeamReader.get_team_name_by_id(winning_team),
        'losing_team': TeamReader.get_team_name_by_id(losing_team)
    }

loss_vals = []
correct_picks = 0
total_picks = 0
for i in range(len(results_seasons)):
    winning_team = results_winning_team[i]
    losing_team = results_losing_team[i]
    season = results_seasons[i]
    loss = get_loss(winning_team, losing_team, season)
    if loss is None:
        continue
    loss_vals.append(loss['loss'])
    if loss['correct']:
        correct_picks += 1
    total_picks += 1
    print(loss)

sum = 0
num_vals = 0
for i in range(len(loss_vals)):
    if loss_vals[i] is not None:
        num_vals += 1
        sum += loss_vals[i]

print("Average Loss: {}".format(sum/num_vals))
print("Correct Picks: {}/{}".format(correct_picks, total_picks))