import nba_api.stats.endpoints as nba_api
from tool_parser import parse_data_frame
from typing import TypedDict, Annotated, Optional, Union, Literal
import pandas as pd

def get_player_game_log(
        player_id: Annotated[int, "The id of the player's games to search for"],
        season: Annotated[str, "The NBA season to search, ex) '2025-26'"],
        date_from: Annotated[Optional[str], "The starting date in a filtered range. format: YYYY-MM-DD"] = None,
        date_to: Annotated[Optional[str], "The ending date in a filtered range. format: YYYY-MM-DD"] = None,
        opponent_abbreviations: Annotated[Optional[list[str]], "List of opponent team abbreviations to filter by (e.g. ['LAL', 'PHX'])"] = None,
        last_n_games: Annotated[Optional[int], "For filtering out the last n games"] = None
        ) -> pd.DataFrame:
    res = nba_api.PlayerGameLog(player_id=player_id, season=season, date_from_nullable=date_from, date_to_nullable=date_to)
    df = res.get_data_frames()[0]

    # check if we want to filter out by the latest games
    if last_n_games != None:
        df = df.head(last_n_games)
    
    # check if we want to filter out by opponents
    if opponent_abbreviations:
        # combine all the abbreviations with a OR in a regex pattern
        pattern = '|'.join(opponent_abbreviations)
        df = df[df['MATCHUP'].str.contains(pattern, case=False, na=False)]
    
    cols = {
        'Game_ID' : 'game_id', 
        'GAME_DATE' : 'game_date',
        'MATCHUP' : 'game_teams'
    }

    return parse_data_frame(df, cols)

def get_team_game_log(
        team_id: Annotated[int, "The id of the team's games to search for"],
        season: Annotated[str, "The NBA season to search, ex) '2025-26'"],
        date_from: Annotated[Optional[str], "The starting date in a filtered range. format: YYYY-MM-DD"] = None,
        date_to: Annotated[Optional[str], "The ending date in a filtered range. format: YYYY-MM-DD"] = None,
        opponent_abbreviations: Annotated[Optional[list[str]], "List of opponent team abbreviations to filter by (e.g. ['LAL', 'PHX'])"] = None,
        last_n_games: Annotated[Optional[int], "For filtering out the last n games"] = None
        ) -> pd.DataFrame:
    res = nba_api.TeamGameLog(player_id=team_id, season=season, date_from_nullable=date_from, date_to_nullable=date_to)
    df = res.get_data_frames()[0]

    # check if we want to filter out by the latest games
    if last_n_games != None:
        df = df.head(last_n_games)
    
    # check if we want to filter out by opponents
    if opponent_abbreviations:
        # combine all the abbreviations with a OR in a regex pattern
        pattern = '|'.join(opponent_abbreviations)
        df = df[df['MATCHUP'].str.contains(pattern, case=False, na=False)]
    
    cols = {
        'Game_ID' : 'game_id', 
        'GAME_DATE' : 'game_date',
        'MATCHUP' : 'game_teams'
    }

    return parse_data_frame(df, cols)

BoxScoreType = Literal[
    'traditional',
    'advanced',
    'hustle',
    'misc',
    'tracking'
]