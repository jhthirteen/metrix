import nba_api.stats.endpoints as nba_api
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.static.teams import find_teams_by_full_name
from tool_parser import parse_data_frame
import pandas as pd
from typing import TypedDict, Annotated, Optional, Union

def get_player_ids(names: Annotated[list[str], "Names of player ids to get, ex) ['LeBron James', 'Jayson Tatum']"]) -> list[int]:
    ids = []
    for name in names:
        res = find_players_by_full_name(name)
        # if the query resulted in no matches, throw an error
        if( not res ):
            raise ValueError("Player does not exist")
        ids.append(res[0]['id'])
    
    return ids

def get_team_ids(names: Annotated[list[str], "Names of team ids to get, ex) ['Lakers', 'Celtics']"]) -> list[int]:
    ids = []
    for name in names:
        res = find_teams_by_full_name(name)
        # if the query resulted in no matches, throw an error
        if( not res ):
            raise ValueError("Team does not exist")
        ids.append(res[0]['id'])
    
    return ids

# schema for the types of fields returned by the player info / bio tool 
class PlayerDict(TypedDict):
    player_id: int
    full_name: str
    birthdate: str
    college: str
    height: str
    weight: str
    seasons_played: int
    jersey_number: str
    team_id: int
    team_name: str
    team_city: str
    year_drafted: str
    last_year_playing: int
    draft_round: str
    draft_pick: str
    active: str

def get_common_player_info(player_id: Annotated[list[int], "List of player ids to get information from"]) -> list[list[PlayerDict]]:
    info = []
    for pid in player_id:
        res = nba_api.CommonPlayerInfo(player_id=pid)
        # capture a response dataframe
        df = res.get_data_frames()[0]
        cols = {
            "PERSON_ID" : "player_id",
            "DISPLAY_FIRST_LAST" : "full_name",
            "BIRTHDATE" : "birthdate",
            "SCHOOL" : "college",
            "HEIGHT" : "height",
            "WEIGHT" : "weight",
            "SEASON_EXP" : "seasons_played",
            "JERSEY" : "jersey_number",
            "TEAM_ID" : "team_id",
            "TEAM_NAME" : "team_name",
            "TEAM_CITY" : "team_city",
            "DRAFT_YEAR" : "year_drafted",
            "TO_YEAR" : "last_year_playing",
            "DRAFT_ROUND" : "draft_round",
            "DRAFT_NUMBER" : "draft_pick",
            "ROSTERSTATUS" : "active",
        }

        info.append(parse_data_frame(df, cols))
    
    return info

class TeamDict(TypedDict):
    team_id: int
    season: str
    city: str
    team_name: str
    conference: str
    division: str
    wins: int
    losses: int
    win_pct: float
    conference_standing: int
    division_standing: int


def get_common_team_info_season(team_ids: Annotated[list[int], "List of team ids to get information from"]) -> list[list[TeamDict]]:
    info = []
    for tid in team_ids:
        res = nba_api.TeamInfoCommon(team_id=tid)
        # capute a response dataframe
        df = res.get_data_frames()[0]
        cols = {
            "TEAM_ID" : "team_id",
            "SEASON_YEAR" : "season",
            "TEAM_CITY" : "city",
            "TEAM_NAME" : "team_name",
            "TEAM_CONFERENCE" : "conference",
            "TEAM_DIVISION" : "division",
            "W" : "wins",
            "L" : "losses",
            "PCT" : "win_pct",
            "CONF_RANK" : "conference_standing",
            "DIV_RANK" : "division_standing"
        }

        info.append(parse_data_frame(df, cols))
    
    return info

def get_team_history(team_ids: Annotated[list[Union[str, int]], "List of team ids to get information from"]):
    team_ids = [int(x) for x in team_ids]
    history = {}
    for tid in team_ids:
        res = nba_api.TeamDetails(team_id=tid)
        df = res.get_data_frames()
        # extract management information
        history['management'] = {
            'owner' : df[0]['OWNER'].item(),
            'general_manager' : df[0]['GENERALMANAGER'].item()
        }
        # extract awards
        awards_cols = {
            "YEARAWARDED" : "year",
            "OPPOSITETEAM" : "opponent"
        }
        history['awards'] = {
            'championships' : parse_data_frame(df[3], awards_cols),
            'conference_finals' : parse_data_frame(df[4], awards_cols),
            'division_champtions' : parse_data_frame(df[5], awards_cols)
        }
        # extract hall of famers
        hof_cols = {
            "PLAYERID" : "player_id",
            "PLAYER" : "player_name",
            "SEASONSWITHTEAM" : "seasons_on_team",
            "YEAR" : "year_inducted"
        }
        history['hall_of_famers'] = {
            'players' : parse_data_frame(df[6], hof_cols)
        }
        # extract retired players
        retired_cols = {
            "PLAYERID" : "player_id",
            "PLAYER" : "player_name",
            "SEASONSWITHTEAM" : "seasons_on_team",
            "JERSEY" : "jersey_num",
            "YEAR" : "year_retired"
        }
        history['retired_jerseys'] = {
            'players' : parse_data_frame(df[7], retired_cols)
        }
    
    return history
        
# schema for the types of fields returned by the roster tool 
class RosterDict(TypedDict):
    player_name: str
    position: str
    age: float
    player_id: int
    acquired_by: str

def get_common_team_roster(team_ids: Annotated[list[int], "List of team ids we want roster information from"], seasons: Annotated[list[str], "List of seasons we want roster information from"]) -> dict[str, dict[int, list[RosterDict]]]:
    info = {}

    for season in seasons:
        # store the season we are searching over as a key
        info[season] = {}
        for tid in team_ids:
            res = nba_api.CommonTeamRoster(team_id=tid, season=season)
            # roster info stored in the 0th data-frame
            df = res.get_data_frames()[0]
            cols = {
                "PLAYER" : "player_name",
                "POSITION" : "position",
                "AGE" : "age",
                "PLAYER_ID" : "player_id",
                "HOW_ACQUIRED" : "acquired_by"
            }
            # map the team id --> roster metadata
            info[season][tid] = parse_data_frame(df, cols)
    
    return info

# schema for the types of fields returned by the coaching tool 
class CoachingDict(TypedDict):
    coach_id: int
    coach_name: str
    coach_type: str

def get_common_team_coaching(team_ids: Annotated[list[int], "List of team ids we want coaching information from"], seasons: Annotated[list[str], "List of seasons we want coaching information from"]) -> dict[str, dict[str, list[CoachingDict]]]:
    info = {}

    for season in seasons:
        # store the season we are searching over as a key
        info[season] = {}
        for tid in team_ids:
            res = nba_api.CommonTeamRoster(team_id=tid, season=season)
            # coaching info stored in the 0th data-frame
            df = res.get_data_frames()[1]
            cols = {
                "COACH_ID" : "coach_id",
                "COACH_NAME" : "coach_name",
                "COACH_TYPE" : "title"
            }
            # map the team id --> roster metadata
            info[season][tid] = parse_data_frame(df, cols)
    
    return info

def search_player_index_season(
        season: Annotated[str, "The NBA season to search, ex) '2025-26'"],
        college: Annotated[Optional[str], "Filter by college, ex) 'Duke'"] = None,
        country: Annotated[Optional[str], "Filter by country, ex) 'USA'"] = None,
        draft_round: Annotated[Optional[str], "Filter by draft round, ex) '2'"] = None,
        draft_year: Annotated[Optional[str], "Filter by draft year, ex) '2003'"] = None,
        draft_pick: Annotated[Optional[str], "Filter by draft pick, ex) '1'"] = None,
        physical: Annotated[Optional[str], "Filter by height, weight, or position, ex) '6'3, '240', or 'SG'"] = None,
        team: Annotated[Optional[str], "Filter by team city or team name, ex) 'Los Angeles', or 'Lakers'"] = None,
        jersey: Annotated[Optional[str], "Filter by jersey number ex)  '0'"] = None
 ):
    
    # set the params
    params = {}
    if college: params["college"] = college
    if country: params["country"] = country
    if draft_round: params["draft_round"] = draft_round
    if draft_year: params["draft_year"] = draft_year
    if draft_pick: params["draft_pick"] = draft_pick
    if physical: params["physical"] = physical
    if team: params["team"] = team
    if jersey: params["jersey"] = jersey

    return player_index_season_helper(season=season, **params)

def search_player_index_history(
        college: Annotated[Optional[str], "Filter by college, ex) 'Duke'"] = None,
        country: Annotated[Optional[str], "Filter by country, ex) 'USA'"] = None,
        draft_round: Annotated[Optional[str], "Filter by draft round, ex) '2'"] = None,
        draft_year: Annotated[Optional[str], "Filter by draft year, ex) '2003'"] = None,
        draft_pick: Annotated[Optional[str], "Filter by draft pick, ex) '1'"] = None,
        physical: Annotated[Optional[str], "Filter by height, weight, or position, ex) '6'3, '240', or 'SG'"] = None,
        team: Annotated[Optional[str], "Filter by team city or team name, ex) 'Los Angeles', or 'Lakers'"] = None,
        jersey: Annotated[Optional[str], "Filter by jersey number ex)  '0'"] = None
 ):
    
    # set the params
    params = {}
    if college: params["college"] = college
    if country: params["country"] = country
    if draft_round: params["draft_round"] = draft_round
    if draft_year: params["draft_year"] = draft_year
    if draft_pick: params["draft_pick"] = draft_pick
    if physical: params["physical"] = physical
    if team: params["team"] = team
    if jersey: params["jersey"] = jersey

    return player_index_history_helper(**params)

# NOTE: think of how we can extend the tool's capabilities to search for things like stats, ranges between years, etc. 
def player_index_season_helper(season: str, **search_modes):
    search_mode_scopes = {
        "college" : ["COLLEGE"],
        "country" : ["COUNTRY"],
        "draft_round" : ["DRAFT_ROUND"],
        "draft_year" : ["DRAFT_YEAR"],
        "draft_pick" : ["DRAFT_NUMBER"],
        "physical" : ["HEIGHT", "WEIGHT", "POSITION"],
        "team" : ["TEAM_CITY", "TEAM_NAME"],
        "jersey" : ["JERSEY_NUMBER"]
    }
    # fetch all possible players to match 
    res = nba_api.PlayerIndex(season=season, historical_nullable=0)
    df = res.get_data_frames()[0]
    
    # sanitize NaN number out
    nan_cols = ["DRAFT_YEAR", "DRAFT_ROUND", "DRAFT_NUMBER", "JERSEY_NUMBER"]
    for col in nan_cols:
        if col in df.columns:
            # convert NaN safely to -1
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int).astype(str)
    
    # start filtering down the dataframe by applying the search_modes
    error_log = []
    df_mask = pd.Series([True] * len(df))
    for search_mode, query in search_modes.items():
        # ensure we are tesitng a valid filter
        if search_mode not in search_mode_scopes:
            error_log.append(f"search_mode: {search_mode} is not a valid criteria for searching.")
            continue
            
        # extract the columns we are filtering over, and a series mask to apply to the larger dataframe
        cols_to_search = search_mode_scopes[search_mode]
        sub_mask = pd.Series([False] * len(df))

        for col in cols_to_search:
            # ensure we are hitting a valid column
            if col not in df.columns:
                error_log.append(f"column name: {col} not in the larger dataframe")
                continue

            # search for a match
            matches = df[col].astype(str).str.lower() == str(query).lower()
            # strip down the sub-mask to only contain matches by OR-ing with the overall mask
            sub_mask = sub_mask | matches

        # strip down the larger mask to only contain matches of all the search columns
        df_mask = df_mask & sub_mask
    
    # apply the mask
    df = df[df_mask]
    cols = {
    "PERSON_ID" : "player_id",
    "PLAYER_LAST_NAME" : "last_name",
    "PLAYER_FIRST_NAME" : "first_name",
    }
    return parse_data_frame(df, cols)

def player_index_history_helper(**search_modes):
    search_mode_scopes = {
        "college" : ["COLLEGE"],
        "country" : ["COUNTRY"],
        "draft_round" : ["DRAFT_ROUND"],
        "draft_year" : ["DRAFT_YEAR"],
        "draft_pick" : ["DRAFT_NUMBER"],
        "physical" : ["HEIGHT", "WEIGHT", "POSITION"],
        "team" : ["TEAM_CITY", "TEAM_NAME"],
        "active" : ["ROSTER_STATUS"],
        "year" : ["FROM_YEAR", "TO_YEAR"],
        "stats" : ["PTS", "REB", "AST"],
        "jersey" : ["JERSEY_NUMBER"]
    }
    # fetch all possible players to match 
    res = nba_api.PlayerIndex(historical_nullable=1)
    df = res.get_data_frames()[0]
    
    # sanitize NaN number out
    nan_cols = ["DRAFT_YEAR", "DRAFT_ROUND", "DRAFT_NUMBER", "JERSEY_NUMBER"]
    for col in nan_cols:
        if col in df.columns:
            # convert NaN safely to -1
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int).astype(str)
    
    # start filtering down the dataframe by applying the search_modes
    error_log = []
    df_mask = pd.Series([True] * len(df))
    for search_mode, query in search_modes.items():
        # ensure we are tesitng a valid filter
        if search_mode not in search_mode_scopes:
            error_log.append(f"search_mode: {search_mode} is not a valid criteria for searching.")
            continue
            
        # extract the columns we are filtering over, and a series mask to apply to the larger dataframe
        cols_to_search = search_mode_scopes[search_mode]
        sub_mask = pd.Series([False] * len(df))

        for col in cols_to_search:
            # ensure we are hitting a valid column
            if col not in df.columns:
                error_log.append(f"column name: {col} not in the larger dataframe")
                continue

            # search for a match
            matches = df[col].astype(str).str.lower() == str(query).lower()
            # strip down the sub-mask to only contain matches by OR-ing with the overall mask
            sub_mask = sub_mask | matches

        # strip down the larger mask to only contain matches of all the search columns
        df_mask = df_mask & sub_mask
    
    # apply the mask
    df = df[df_mask]
    cols = {
    "PERSON_ID" : "player_id",
    "PLAYER_LAST_NAME" : "last_name",
    "PLAYER_FIRST_NAME" : "first_name",
    }
    return parse_data_frame(df, cols)