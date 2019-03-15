import pandas as pd
import os

from modules.models.team import Team
from modules.models.kenpom_data import KenPom

file_path = os.path.dirname(__file__)
teams_input_file = os.path.join(file_path, '../../data/DataFiles/Teams.csv')
teams_spelling_file = os.path.join(file_path, '../../data/DataFiles/TeamSpellings.csv')
kenpom_file = os.path.join(file_path, '../../data/DataFiles/kenpom.csv')
kenpom_map = os.path.join(file_path, '../../data/DataFiles/kenpom_map_v2.csv')

class TeamReader:

    def __init__(self):
        self.teams = {}

    def getTeamData(self, team_id):
        #makes dictionary of team_from kaggle data
        self.get_teams()

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
        data = pd.read_csv(kenpom_map)
        for i in range(len(team_names)):
            team_name = team_names[i]
            team_id = team_ids[i]
            start_season = start_seasons[i]
            end_season = end_seasons[i]
            for year in range(start_season, end_season+1):
                #TODO: need to remove 2019 for future prediction
                if year < 2002 or year == 2019:
                    continue
                x = self.getTeamDataBySeason(data, team_id, year)
                if x is None:
                    continue
                kenpom_data = KenPom(x['Rk'].values[0], x['Seed'].values[0], x['Conf'].values[0], x['AdjEM'].values[0],
                                     x['AdjO'].values[0], x['AdjO_rank'].values[0], x['AdjD'].values[0],
                                     x['AdjD_rank'].values[0], x['AdjT'].values[0], x['AdjT_rank'].values[0],
                                     x['Luck'].values[0], x['Luck_rank'].values[0], x['AdjEM.1'].values[0],
                                     x['AdjEM_rank'].values[0], x['OppO'].values[0], x['OppO_rank'].values[0],
                                     x['OppD'].values[0], x['OppD_rank'].values[0], x['AdjEM.2'].values[0])
                team = Team(year, team_id, team_name, kenpom_data)
                self.teams[team.id] = team
        return self.teams

    def getTeamDataBySeason(self, data, team_id, team_year):
        result = data.loc[((data['Season'] == team_year) & (data['TeamID'] == team_id))].any()
        # result['Team'] will be false if no items met the criteria above
        if not result['Team']:
            data_team = None
        else:
            data_team = data.loc[(data['Season'] == team_year) & (data['TeamID'] == team_id)]

        return data_team

    def getTeamCode(self):
        #finds associated team code with team name reported on csv input file
        pass

    def generateCSVTeamDict(self, starting_year, seasons):
        '''
        loops through all team names across all 17 seasons and generates a dictionary with key=teamName and
        value= teamID
        :return:
        '''


    def checkExcelSheets(self, starting_year, seasons):
        '''
        checks excel file to make sure deletion of header rows done correctly
        returns: (boolean) True if okay, False otherwise
        '''
        season_years = []
        for x in range(seasons):
            season_years.append(starting_year + x)

        #stores any errors from all files
        errors = []

        for year in season_years:
            input_file = '../../data/%s.csv' % year
            data = pd.read_csv(input_file)
            for x in range(len(data) - 1):
                if data['Rk'][x] != x + 1:
                    #appends an array [file name, row]
                    errors.append([input_file, x])
                    print('got unexpected rank: row {} in {}'.format(x, input_file))

        if len(errors) != 0:
            print('errors: {}'.format(errors))
            return False
        else:
            return True

    @staticmethod
    def addSeedColumn(starting_year, seasons):
        """
        function to get the kenpom data from raw_data, no need to call in the future.
        call (2002, 17) to get current data. may need to update every year.
        output: kenpom.csv
        """
        years = []
        for x in range(seasons):
            years.append(starting_year + x)
        data_list = []
        count = 0
        for year in years:
            input_file = '../data/%s.csv' % year
            data = pd.read_csv(input_file, encoding="ISO-8859-1")
            name_items =[i.split('?') for i in data['Team']]
            data['Team'] = [i[0] for i in name_items]
            data['Seed'] = [i[1] if len(i)>1 else None for i in name_items ]
            data['Season'] = year
            count += len(data)
            data_list.append(data)
        df = pd.concat(data_list)
        df = df.drop('W-L', axis=1) # drop W-L since there are wrong values. treating some value as date format
        df.to_csv("../data/DataFiles/kenpom.csv", index=False)

    @staticmethod
    def map_kenpom_data():
        """
        map kenpom_data. used kenpom.csv and teamspelling.csv
        :return: write to a new csv
        """
        data = pd.read_csv(kenpom_file)
        data['Team'] = data['Team'].str.lower()
        teams = pd.read_csv(teams_spelling_file, encoding="ISO-8859-1")
        teams.rename(columns = {'TeamNameSpelling':'Team'},inplace = True)
        new_data = data.merge(teams, on='Team', how='left')
        new_data.to_csv("../data/DataFiles/kenpom_map_v1.csv", index=False)
