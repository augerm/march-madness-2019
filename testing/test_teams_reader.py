from modules.services.teams_reader import TeamReader

# def test_add_seeds():
#     TeamReader.addSeedColumn(2002, 17)


def test_map_kenpom_file():
    TeamReader.map_kenpom_data()