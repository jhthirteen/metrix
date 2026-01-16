import nba_api.stats.endpoints as nba_api
from tool_parser import parse_data_frame, parse_data_frame_exclude
from typing import TypedDict, Annotated, Optional, Union, Literal, Any
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
    'defensive',
    'four_factors',
    'player_tracking',
    'scoring',
    'usage'
]

BoxScoreSearchType = Literal[
    'player',
    'team'
]

endpoint_map = {
    'traditional' : nba_api.BoxScoreTraditionalV3,
    'advanced' : nba_api.BoxScoreAdvancedV3,
    'hustle' : nba_api.BoxScoreHustleV2,
    'misc' : nba_api.BoxScoreMiscV3,
    'defensive' : nba_api.BoxScoreDefensiveV2,
    'four_factors' : nba_api.BoxScoreFourFactorsV3,
    'player_tracking' : nba_api.BoxScorePlayerTrackV3,
    'scoring' : nba_api.BoxScoreScoringV3,
    'usage' : nba_api.BoxScoreUsageV3
}

search_type_map = {
    'player' : 0,
    'team' : 1
}

search_type_exclude_cols = {
    'player' : {'gameId', 'teamTricode', 'teamSlug', 'nameI', 'playerSlug', 'comment', 'jerseyNum'},
    'team' : {'gameId', 'teamTricode', 'teamSlug'}
}

team_metadata = {'teamId', 'teamName', 'teamCity'}

def get_game_box_score(
        game_id: Annotated[str, "The 10-digit Game ID (e.g. '0022300123') retrieved from game logs."],
        stat_type: Annotated[BoxScoreType, "The specific category of stats to retrieve. Options:\n"
        "- 'traditional': Standard stats (PTS, REB, AST, STL, BLK).\n"
        "- 'advanced': Efficiency metrics (OFF_RTG, DEF_RTG, PACE, PIE).\n"
        "- 'defensive': Matchup defense stats (Contested Shots, Def FG%).\n"
        "- 'four_factors': Team success factors (EFG%, TOV%, OREB%, FTA Rate).\n"
        "- 'hustle': Effort plays (Screen Assists, Deflections, Box Outs, Charges Drawn).\n"
        "- 'misc': Game flow (Points in Paint, 2nd Chance Pts, Fast Break Pts).\n"
        "- 'player_track': Movement data (Distance Traveled, Average Speed, Touches).\n"
        "- 'scoring': Granular scoring (Pct of Team Pts, Pts from Midrange/Paint).\n"
        "- 'usage': Usage rates (USG%, Pct of Team Plays Used)."] = 'traditional',
        search_type: Annotated[BoxScoreSearchType, "The type of box-score you want to retrieve (player vs. whole team). Options: 'player' or 'team'"] = 'player'
) -> dict[str, Any]:
    # check to ensure we are calling a valid box-score type
    if stat_type not in endpoint_map:
        raise ValueError(f'Invalid argument for stat_type: {stat_type}')
    
    if search_type not in search_type_map:
        raise ValueError(f'Invalid argument for search_type: {search_type}')

    # call the desired endpoint
    endpoint = endpoint_map[stat_type]
    res = endpoint(game_id)

    # convert to df --> get either player or team box score depending on search_type 
    df = res.get_data_frames()[search_type_map[search_type]]
    # parse out columns we dont care about 
    cols = search_type_exclude_cols[search_type]
    raw_data = parse_data_frame_exclude(df, cols)

    # clean up the data and group the box score by each team
    cleaned_data = {}
    for row in raw_data:
        team_key = f'{row["teamCity"]} {row["teamName"]}'
        
        # check for team key membership to output data
        if team_key not in cleaned_data:
            cleaned_data[team_key] = {
                'team_id' : row["teamId"],
                'player_stats' : []
            }
        
        # filter out the player data we want --> append to the list
        player_stats = {key : val for key, val in row.items() if key not in team_metadata}
        cleaned_data[team_key]['player_stats'].append(player_stats)
    
    return cleaned_data

AggregatedStatsType = Literal['base', 'advanced', 'misc', 'scoring', 'usage', 'defense']

def get_aggregated_player_stats(
    player_id: Annotated[int, "The id of the player's games to search for"],
    season: Annotated[str, "The NBA season to search, ex) '2025-26'"],
    stat_type: Annotated[AggregatedStatsType, "The category of stats to filter by and receive"],
    last_n_games: Annotated[Optional[int], "For filtering out the last n games"] = None
) -> str:
    pass