import pandas as pd

from modules.models.team import Team

teams_input_file = '../data/DataFiles/Teams.csv'
data_input_file = '../../data/2018.csv'

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
        for i in range(len(team_names)):
            team_name = team_names[i]
            team_id = team_ids[i]
            start_season = start_seasons[i]
            end_season = end_seasons[i]
            for year in range(start_season, end_season+1):
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

    def addSeedColumn(self, starting_year, seasons):
        years = []
        for x in range(seasons):
            years.append(starting_year + x)

        for year in years:
            input_file = '../../data/%s.csv' % year
            data = pd.read_csv(input_file)
            data.insert(2, 'Seed', 99999)
            for x in range(len(data) - 1):
                name_items = data['Team'][x].split('\xa0')
                #all teams len(name_items) == 2 should have a seed
                if len(name_items) == 2:
                    data['Seed'][x] = name_items[1]
                else:
                    data['Seed'][x] = None

                #set string in team column to team's name
                data['Team'][x] = name_items[0]
                print('Team: {} Regional Seed: {}'.format(data['Team'][x], data['Seed'][x]))
            data.to_csv('../../data_2/%s_2.csv' % year)

    addSeedColumn(2002, 17)

    # def renameUnnamedColumns(self):
    #     '''
    #     renames columns that are currently unnamed
    #     :return:
    #     '''