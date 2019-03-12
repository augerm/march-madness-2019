import pandas as pd

from modules.models.team import Team

teams_input_file = '../data/DataFiles/Teams.csv'
data_input_file = '../../data/2018.csv'

class TeamReader:

    def __init__(self):
        self.teams = {}

    def update_result(self, result):
        self.predicted_result = result

    def get_teams(self):
        if self.teams.keys():
            return self.teams
        teams_df = pd.read_csv(teams_input_file)
        team_names = list(teams_df['TeamName'])
        team_ids = list(teams_df['TeamID'])
        start_seasons = list(teams_df['FirstD1Season'])
        end_seasons = list(teams_df['LastD1Season'])
        for i in range(len(team_names)):
            team_name = team_names[i]
            team_id = team_ids[i]
            start_season = start_seasons[i]
            end_season = end_seasons[i]
            for year in range(start_season, end_season):
                team = Team(year, team_id, team_name)
                self.teams[team.id] = team
        return self.teams

    def getTeamDataBySeason(self):
        seasons = 1
        start_season = 2018
        season_years = []
        for x in range(seasons):
            season_years.append(int(start_season + x))
        for year in season_years:
            input_file = '../../data/2018'
            data = pd.read_csv(data_input_file, skiprows=1)
            for x in range(len(data)):
                data_team = data.loc[data['Rk'] == x + 1]
                team_name = data[x]['Team']
                self.getTeamCode(team_name)
                print(team_name)

    def getTeamCode(self):
        #finds associated team code with team name reported on csv input file
        pass

    def getTeamData(self):
        data = pd.read_csv(data_input_file, skiprows=1)
        # for x in range(len(data)):
        data_ex = data.loc[data['Rk'] == 1]
        my_name = data_ex['Team']
        print(my_name)