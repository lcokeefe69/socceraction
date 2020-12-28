
import os

import pandas as pd
import pytest
from socceraction.spadl import config as spadl
from socceraction.spadl import opta as opta
from socceraction.spadl.base import SPADLSchema
from socceraction.spadl.opta import (OptaCompetitionSchema, OptaEventSchema,
                                     OptaGameSchema, OptaPlayerSchema,
                                     OptaTeamSchema)


class TestJSONOptaLoader:

    def setup_method(self):
        data_dir = '/cw/dtaidata/ml/2019-DTAISportsAnalyticsLab/soccer-opta/raw-xml'
        self.loader = opta.OptaLoader(root=data_dir, parser="json", feeds={
            'f1': "tournaments/tournament-{season_id}-{competition_id}.json",
            'f9': "matches/match-{season_id}-{competition_id}-{game_id}.json",
            'f24': "matches/match-{season_id}-{competition_id}-{game_id}.json"})

    def test_competitions(self):
        df_competitions = self.loader.competitions()
        assert len(df_competitions) > 0
        OptaCompetitionSchema.validate(df_competitions)

    def test_games(self):
        df_games = self.loader.games(8, 2016)
        assert len(df_games) == 380
        OptaGameSchema.validate(df_games)

    def test_teams(self):
        df_teams = self.loader.teams(918893)
        assert len(df_teams) == 2
        OptaTeamSchema.validate(df_teams)

    def test_players(self):
        df_players = self.loader.players(918893)
        assert len(df_players) == 27
        OptaPlayerSchema.validate(df_players)

    def test_events(self):
        df_events = self.loader.events(918893)
        assert len(df_events) > 0
        OptaEventSchema.validate(df_events)


class TestXMLOptaLoader:

    def setup_method(self):
        data_dir = '/cw/dtaijupiter/NoCsBack/dtai/pieterr/Data/soccer-opta-xml/ftp.performgroup.com/'

        self.loader = opta.OptaLoader(root=data_dir, parser="xml", feeds={
            'f7': "La Liga/srml-{competition_id}-{season_id}-f{game_id}-matchresults.xml",
            'f24': "La Liga/f24-{competition_id}-{season_id}-{game_id}-eventdetails.xml"})

    def test_competitions(self):
        df_competitions = self.loader.competitions()
        assert len(df_competitions) > 0
        OptaCompetitionSchema.validate(df_competitions)

    def test_games(self):
        df_games = self.loader.games(23, 2018)
        assert len(df_games) == 380
        OptaGameSchema.validate(df_games)

    def test_teams(self):
        df_teams = self.loader.teams(1009316)
        assert len(df_teams) == 2
        OptaTeamSchema.validate(df_teams)

    def test_players(self):
        df_players = self.loader.players(1009316)
        assert len(df_players) == 36
        OptaPlayerSchema.validate(df_players)

    def test_events(self):
        df_events = self.loader.events(1009316)
        assert len(df_events) > 0
        OptaEventSchema.validate(df_events)

class TestSpadlConvertor():

    def setup_method(self):
        data_dir = '/cw/dtaijupiter/NoCsBack/dtai/pieterr/Data/soccer-opta-xml/ftp.performgroup.com/'
        loader = opta.OptaLoader(root=data_dir, parser="xml", feeds={
            'f7': "La Liga/srml-{competition_id}-{season_id}-f{game_id}-matchresults.xml",
            'f24': "La Liga/f24-{competition_id}-{season_id}-{game_id}-eventdetails.xml"})
        self.events = loader.events(1009316)

    def test_convert_to_actions(self):
        df_actions = opta.convert_to_actions(self.events, 174)
        assert len(df_actions) > 0
        SPADLSchema.validate(df_actions)
        assert (df_actions.game_id == 1009316).all()
        assert ((df_actions.team_id == 174) | (df_actions.team_id == 957)).all()

