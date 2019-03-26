import os
import pandas as pd
from zipfile import ZipFile
import requests
import json

competition_name = 'mens-machine-learning-competition-2019'
file_name = "{}.zip".format(competition_name)
leaderboard_name = "{}-publicleaderboard.csv".format(competition_name)

api_df = pd.read_csv('api_url.config', sep=",") # api_url.config should be added locally.

team_name = 'blue jerseys'
api_url = api_df[api_df['name']=='slack_hook_api']['url'].values[0]
print(api_url)
def get_rank_message():
    messages = []
    os.system('kaggle competitions leaderboard {} --download'.format(competition_name))
    with ZipFile(file_name, 'r') as zip:
        zip.extractall()
    leaderboard = pd.read_csv(leaderboard_name)
    our_scores = leaderboard[leaderboard['TeamName']=='blue jerseys']
    message1 = ""
    for ind in our_scores.index:
        message1 = message1 + "{} {:.4f} ".format(str(our_scores.loc[ind]['SubmissionDate']), our_scores.loc[ind]['Score'])  
    score1_leaderboard = leaderboard.groupby('TeamName').min()
    score1_leaderboard = score1_leaderboard.sort_values('Score').reset_index()
    info1 = score1_leaderboard[score1_leaderboard['TeamName']=='blue jerseys']
    rank = info1.index[0]
    score = info1['Score'].values[0]
    messages.append(message1)
    messages.append("our ranking {}, score {:.4f}".format(rank, score))
    return messages


def send_slack_message(messages):
    if not messages:
        return None
    for message in messages:
        data ={'text':message}
        headers = {'content-type': 'application/json'}
        print(message)
        # requests.post(api_url,data=json.dumps(data), headers= headers)


def run():
    message = get_rank_message()
    send_slack_message(message)


if __name__ == '__main__':
    run()
