import nba_api.stats.endpoints as nba_api
from tool_parser import parse_data_frame
from nba_api.stats.static.teams import find_teams_by_full_name
from typing import TypedDict, Annotated, Optional, Union, Literal
from enum import Enum

def get_team_ids(names: Annotated[list[str], "Names of team ids to get, ex) ['Lakers', 'Celtics']"]) -> list[int]:
    ids = []
    for name in names:
        res = find_teams_by_full_name(name)
        # if the query resulted in no matches, throw an error
        if( not res ):
            raise ValueError("Team does not exist")
        ids.append(res[0]['id'])
    
    return ids

class AllTimeStat(Enum):
    games_played = 0
    points = 1
    assists = 2
    steals = 3
    offensive_rebounds = 4
    defensive_rebounds = 5
    rebounds = 6
    blocks = 7
    field_goals_made = 8
    field_goals_attempted = 9
    field_goal_percentage = 10
    turnovers = 11
    three_pointers_made = 12
    three_pointers_attempted = 13
    three_pointer_percentage = 14
    personal_fouls = 15
    free_throws_made = 16
    free_throws_attempted = 17
    free_throw_percentage = 18

def get_all_time_leader(stat: Annotated[AllTimeStat, "stat that we are searching for all-time leaders in"], top_x: Annotated[int, "Number of top players we are searching for. ex) top 3 scorers in NBA history."]) -> dict[str, Union[str, int]]:
    res = nba_api.AllTimeLeadersGrids(topx=top_x)
    # capture the dataframe associated with the stat in the query
    df = res.get_data_frames()[stat.value]
    cols = {
        "PLAYER_ID" : "player_id",
        "PLAYER_NAME" : "player_name",
        df.columns[2] : "stat_value",
        df.columns[3] : "all_time_rank"
    }

    return parse_data_frame(df, cols)

FranchiseLeaderStat = Literal['points', 'assists', 'rebounds', 'blocks', 'steals']
# 2. Update map to use string keys
stat_column_map = {
    'points': {
        "PTS": 'points',
        "PTS_PERSON_ID": 'pts_player_id',
        "PTS_PLAYER": 'pts_player_name'
    },
    'assists': {
        "AST": 'assists',
        "AST_PERSON_ID": 'ast_player_id',
        "AST_PLAYER": 'ast_player_name'
    },
    'rebounds': {
        "REB": 'rebounds',
        "REB_PERSON_ID": 'reb_player_id',
        "REB_PLAYER": 'reb_player_name'
    },
    'blocks': {
        "BLK": 'blocks',
        "BLK_PERSON_ID": 'blk_player_id',
        "BLK_PLAYER": 'blk_player_name'
    },
    'steals': {
        "STL": 'steals',
        "STL_PERSON_ID": 'stl_player_id',
        "STL_PLAYER": 'stl_player_name'
    }
}

def get_team_stat_leader(team_id: Annotated[int, "Team ID to get information from"], stats: Annotated[list[FranchiseLeaderStat], "List of stats to get the franchise leader of"]) -> dict[str, Union[str, int]]:
    res = nba_api.FranchiseLeaders(team_id)
    df = res.get_data_frames()[0]
    cols = {}
    # combine each dictionary for each stat that we are searching over
    for stat in stats:
        cols = cols | stat_column_map[stat]

    return parse_data_frame(df, cols)

StatLiteral = Literal[
    "MIN",
    "FGM",
    "FGA",
    "FG_PCT",
    "FG3M",
    "FG3A",
    "FG3_PCT",
    "FTM",
    "FTA",
    "FT_PCT",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "PTS",
    "EFF",
    "AST_TOV"
]

def get_stat_leader_totals_season(season: Annotated[str, "The NBA season to search, ex) '2025-26'"], stat: Annotated[StatLiteral, "The statistical category to find leaders for"], top_x: Annotated[int, "The x number of top players you want to search for"]) -> dict[str, Union[str, int]]:
    res = nba_api.LeagueLeaders(season=season, stat_category_abbreviation=stat)
    df = res.get_data_frames()[0].head(top_x)
    cols = {
        "PLAYER_ID" : "player_id",
        "PLAYER" : "player_name",
        "RANK" : "stat_rank",
        stat : "stat_value"
    }

    return parse_data_frame(df, cols)

    

def get_stat_leader_averages_season(season: Annotated[str, "The NBA season to search, ex) '2025-26'"], stat: Annotated[StatLiteral, "The statistical category to find leaders for"], top_x: Annotated[int, "The x number of top players you want to search for"]) -> dict[str, Union[str, int]]:
    res = nba_api.LeagueLeaders(season=season, stat_category_abbreviation=stat, per_mode48="PerGame")
    df = res.get_data_frames()[0].head(top_x)
    cols = {
        "PLAYER_ID" : "player_id",
        "PLAYER" : "player_name",
        "RANK" : "stat_rank",
        stat : "stat_value"
    }

    return parse_data_frame(df, cols)

def get_league_standings_season(season: Annotated[str, "The NBA season to search, ex) '2025-26'"] ) -> dict[str, Union[str, int]]:
    res = nba_api.LeagueStandingsV3(season=season)
    df = res.get_data_frames()[0]
    # we have to map rank --> team for each conference
    eastern_conference = {}
    western_conference = {}

    for index, row in df.iterrows():
        if row["Conference"] == "East":
            eastern_conference[row["PlayoffRank"]] = {"team_id" : row["TeamID"], "team_name" : f'{row["TeamCity"]} {row["TeamName"]}'}
        else:
            western_conference[row["PlayoffRank"]] = {"team_id" : row["TeamID"], "team_name" : f'{row["TeamCity"]} {row["TeamName"]}'}
    
    return {
        "eastern_conference_standings" : eastern_conference,
        "western_conference_standings" : western_conference
    }