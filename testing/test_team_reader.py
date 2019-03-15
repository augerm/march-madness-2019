from modules.services.teams_reader import TeamReader

def test_get_team():
    teamreader = TeamReader()
    teamreader.get_teams()
