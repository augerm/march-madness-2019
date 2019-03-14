class KenPom:
    def __init__(self, country_rank, regional_rank, conference, Adj_EM, AdjO, AdjO_rank, AdjD, AdjD_rank, AdjT, AdjT_rank, luck, luck_rank, opp_AdjEM, opp_AdjEM_rank, opp_AdjO, opp_AdjO_rank, opp_AdjD, opp_AdjD_rank, NCSOS):
        self.country_rank = country_rank
        self.regional_rank = regional_rank
        self.conference = conference
        self.efficiency_margin = Adj_EM
        self.offensive_efficiency = AdjO
        self.offensive_efficiency_rank = AdjO_rank
        self.defensive_efficiency = AdjD
        self.defensive_efficiency_rank = AdjD_rank
        self.tempo = AdjT
        self.tempo_rank = AdjT_rank
        self.luck = luck
        self.luck_rank = luck_rank
        self.schedule_efficiency_margin = opp_AdjEM
        self.schedule_efficiency_margin_rank = opp_AdjEM_rank
        self.schedule_offensive_margin = opp_AdjO
        self.schedule_offensive_margin_rank = opp_AdjO_rank
        self.schedule_defensive_margin = opp_AdjD
        self.schedule_defensive_margin_rank = opp_AdjD_rank
        self.non_conference_schedule_efficieny_margin = NCSOS