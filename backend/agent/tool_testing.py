import pytest
from unittest.mock import patch, MagicMock
import identity_tools
import pandas as pd

'''
----- TESTING FOR GET PLAYER / TEAM ID FUNCTIONS -----
'''

# patch in the API call with some mock data
@patch("identity_tools.find_players_by_full_name")
def test_get_player_ids_single_player_success(mock_find_player):
    # define a normal API return value
    mock_find_player.return_value = [{'id': 2544, 'full_name': 'LeBron James', 'first_name': 'LeBron', 'last_name': 'James', 'is_active': True}]
    # call the function normally
    ids = identity_tools.get_player_ids(["LeBron James"])
    # assert correctness
    assert ids == [2544]
    mock_find_player.assert_called_once_with("LeBron James")

@patch("identity_tools.find_players_by_full_name")
def test_get_player_ids_multiple_player_success(mock_find_player):
    mock_find_player.side_effect = [
        [{'id': 2544, 'full_name': 'LeBron James', 'first_name': 'LeBron', 'last_name': 'James', 'is_active': True}],
        [{'id': 201939, 'full_name': 'Stephen Curry', 'first_name': 'Stephen', 'last_name': 'Curry', 'is_active': True}],
        [{'id': 893, 'full_name': 'Michael Jordan', 'first_name': 'Michael', 'last_name': 'Jordan', 'is_active': False}]
    ]

    ids = identity_tools.get_player_ids(["LeBron James", "Stephen Curry", "Michael Jordan"])
    # assert correctness
    assert ids == [2544, 201939, 893]
    assert mock_find_player.call_count == 3

@patch("identity_tools.find_players_by_full_name")
def test_get_player_ids_failure(mock_find_player):
    mock_find_player.return_value = []
    # check that a value error is thrown 
    with pytest.raises(ValueError, match="Player does not exist"):
        identity_tools.get_player_ids("Steph Curry")

@patch("identity_tools.find_teams_by_full_name")
def test_get_team_ids_single_team_success(mock_find_team):
    mock_find_team.return_value = [{'id': 1610612755, 'full_name': 'Philadelphia 76ers', 'abbreviation': 'PHI', 'nickname': '76ers', 'city': 'Philadelphia', 'state': 'Pennsylvania', 'year_founded': 1949}]

    ids = identity_tools.get_team_ids(["76ers"])
    # assert correctness
    assert ids == [1610612755]
    mock_find_team.assert_called_once_with("76ers")

@patch("identity_tools.find_teams_by_full_name")
def test_get_team_ids_multiple_team_success(mock_find_team):
    mock_find_team.side_effect = [
        [{'id': 1610612755, 'full_name': 'Philadelphia 76ers', 'abbreviation': 'PHI', 'nickname': '76ers', 'city': 'Philadelphia', 'state': 'Pennsylvania', 'year_founded': 1949}],
        [{'id': 1610612747, 'full_name': 'Los Angeles Lakers', 'abbreviation': 'LAL', 'nickname': 'Lakers', 'city': 'Los Angeles', 'state': 'California', 'year_founded': 1948}],
        [{'id': 1610612738, 'full_name': 'Boston Celtics', 'abbreviation': 'BOS', 'nickname': 'Celtics', 'city': 'Boston', 'state': 'Massachusetts', 'year_founded': 1946}]
    ]

    ids = identity_tools.get_team_ids(["76ers", "Lakers", "Celtics"])
    # assert correctness
    assert ids == [1610612755, 1610612747, 1610612738]
    assert mock_find_team.call_count == 3

@patch("identity_tools.find_teams_by_full_name")
def test_get_team_ids_failure(mock_find_team):
    mock_find_team.return_value = []

    with pytest.raises(ValueError, match="Team does not exist"):
        identity_tools.get_team_ids(["Supersonics"])

'''
----- TESTING FOR GETTING COMMON PLAYER INFO -----
'''

@patch("identity_tools.nba_api.CommonPlayerInfo")
def test_get_common_player_info_single_success(mock_player_class):
    mock_df = pd.DataFrame([{
            "PERSON_ID": 1628369,
            "FIRST_NAME": "Jayson",
            "LAST_NAME": "Tatum",
            "DISPLAY_FIRST_LAST": "Jayson Tatum",
            "DISPLAY_LAST_COMMA_FIRST": "Tatum, Jayson",
            "DISPLAY_FI_LAST": "J. Tatum",
            "PLAYER_SLUG": "jayson-tatum",
            "BIRTHDATE": "1998-03-03T00:00:00",
            "SCHOOL": "Duke",
            "COUNTRY": "USA",
            "LAST_AFFILIATION": "Duke/USA",
            "HEIGHT": "6-8",
            "WEIGHT": "210",
            "SEASON_EXP": 8,
            "JERSEY": "0",
            "POSITION": "Forward-Guard",
            "ROSTERSTATUS": "Active",
            "GAMES_PLAYED_CURRENT_SEASON_FLAG": "N",
            "TEAM_ID": 1610612738,
            "TEAM_NAME": "Celtics",
            "TEAM_ABBREVIATION": "BOS",
            "TEAM_CODE": "celtics",
            "TEAM_CITY": "Boston",
            "PLAYERCODE": "jayson_tatum",
            "FROM_YEAR": "2017",
            "TO_YEAR": 2025,
            "DLEAGUE_FLAG": "N",
            "NBA_FLAG": "Y",
            "GAMES_PLAYED_FLAG": "Y",
            "DRAFT_YEAR": "2017",
            "DRAFT_ROUND": "1",
            "DRAFT_NUMBER": "3",
            "GREATEST_75_FLAG": "N"
        }])
    
    mock_player_class.return_value.get_data_frames.return_value = [mock_df]

    info = identity_tools.get_common_player_info([1628369])
    expected = [[{'player_id': 1628369, 'full_name': 'Jayson Tatum', 'birthdate': '1998-03-03T00:00:00', 'college': 'Duke', 'height': '6-8', 'weight': '210', 'seasons_played': 8, 'jersey_number': '0', 'team_id': 1610612738, 'team_name': 'Celtics', 'team_city': 'Boston', 'year_drafted': '2017', 'last_year_playing': 2025, 'draft_round': '1', 'draft_pick': '3', 'active': 'Active'}]]
    # assert correctness
    assert info == expected
    mock_player_class.assert_called_once_with(player_id=1628369)