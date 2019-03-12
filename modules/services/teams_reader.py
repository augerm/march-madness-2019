import pandas as pd

data_input_file = '../../data/2018.csv'

class team_reader:

    def __init__(self):
        self.teams = {}

    def update_result(self, result):
        self.predicted_result = result

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

    def getTeamData(self):
        data = pd.read_csv(data_input_file, skiprows=1)
        # for x in range(len(data)):
        data_ex = data.loc[data['Rk'] == 1]
        my_name = data_ex['Team']
        print(my_name)

    getTeamData()