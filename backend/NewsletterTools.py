from nba_api.stats.static import players
import nba_api.stats.endpoints as nba_api
from datetime import date, timedelta
import os
from groq import Groq
from supabase import Client, create_client
import re
import CommonLeagueInfo
import time

#NOTE: need to set up a daily batch job that runs the summary generation

class NewsletterTools:
    def __init__(self):
        self.date = date.today().isoformat()
        self.base_url = "https://stats.nba.com/stats/"
        self.game_ids = {}
        self.game_summaries = {}
        self.west_standings = []
        self.east_standings = []
        self.player_performance_weights = {
            'points' : 1.0,
            'assists' : 0.75,
            'reboundsTotal' : 0.75,
            'plusMinusPoints' : 0.5,
            'blocks' : 0.65,
            'steals' : 0.65,
            'turnovers' : -1.0,
            'threePointersAttempted' : -0.60,
            'threePointersMade' : 0.50,
            'fieldGoalsAttempted' : -0.50,
            'fieldGoalsMade' : 0.40,
            'freeThrowsAttempted' : -0.20,
            'freeThrowsMade' : 0.10
        }

        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.messages = [
            {
                "role" : "system",
                "content" : "You are an expert NBA Analyst that is tasked with providing a high level summary of NBA games. Please stick to only the statistics you are provided with, and do not rely on anything else for numbers you write in the summary. Don't make any assumptions about the data, like game-high, team-high, etc. Ignore all IDs. A summary should have the following format, keep the capitalized words in as headers: SCOREWinnigTeam Score, LosingTeam ScoreDETAILSProvide details of the game.KEY PERFORMERSProvide details of the players who performed the best! Don't just purely write their stats here. Each player should be on their own line starting with -"
            }
        ]
        self.model = "moonshotai/kimi-k2-instruct-0905"

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)

    def get_standings(self) -> None:
        #NOTE: this should be modular so we should not need to hard-code the season... but for now let's do that
        cur_season = "2025-26"
        df = nba_api.LeagueStandingsV3(season=cur_season, season_type="Regular Season").get_data_frames()[0]
        # teams are given in ascending record order --> can simply be appended to each array this way without the need for sorting
        for index, row in df.iterrows():
            # store team ID in these tuples so that we can easily access pictures of each team NOTE TO SELF: maybe make this a database object (idea, these don't really change no reason to fetch every time we want to display)
            if row["Conference"] == "West":
                self.west_standings.append(row["TeamID"])
            elif row["Conference"] == "East":
                self.east_standings.append(row["TeamID"])
            else:
                raise ValueError("Error during data gathering stage for updated NBA Standings.")     

    def get_previous_day_games(self) -> None:
        previous_date = date.today() - timedelta(days=1)
        df = nba_api.ScoreboardV2(game_date=previous_date).get_data_frames()[0]
        # EXTRACT TOTALS WITH STATISTICS
        # loop through each game and extract the ID 
        for index, row in df.iterrows():
            self.game_ids[row["GAME_ID"]] = None

    def get_game_details(self) -> None:
        for id_key in self.game_ids:
            df = nba_api.BoxScoreTraditionalV3(game_id=id_key).get_dict()
            df = df["boxScoreTraditional"]

            home_team_stats = {
                'team_name' : f'{df["homeTeam"]["teamCity"]} {df["homeTeam"]["teamName"]}',
                'team_id' : df["homeTeam"]["teamId"],
                'points' : df["homeTeam"]["statistics"]["points"],
                'field_goals_made' : df["homeTeam"]["statistics"]["fieldGoalsMade"],
                'field_goals_attempted' : df["homeTeam"]["statistics"]["fieldGoalsAttempted"],
                'field_goal_percentage' : df["homeTeam"]["statistics"]["fieldGoalsPercentage"],
                'three_pointers_made' : df["homeTeam"]["statistics"]["threePointersMade"],
                'three_pointers_attempted' : df["homeTeam"]["statistics"]["threePointersAttempted"],
                'three_pointers_percentage' : df["homeTeam"]["statistics"]["threePointersPercentage"],
                'free_throws_made' : df["homeTeam"]["statistics"]["freeThrowsMade"],
                'free_throws_attempted' : df["homeTeam"]["statistics"]["freeThrowsAttempted"],
                'free_throws_percentage' : df["homeTeam"]["statistics"]["freeThrowsPercentage"],
                'rebounds' : df["homeTeam"]["statistics"]["reboundsTotal"],
                'assists' : df["homeTeam"]["statistics"]["assists"],
                'steals' : df["homeTeam"]["statistics"]["steals"],
                'blocks' : df["homeTeam"]["statistics"]["blocks"],
                'turnovers' : df["homeTeam"]["statistics"]["turnovers"],
                'player_stats' : {}
            }


            for player in df["homeTeam"]["players"]:
                id = player["personId"]
                name = f'{player["firstName"]} {player["familyName"]}'
                home_team_stats["player_stats"][name] = player["statistics"]
                # add the players id to the dictionary
                home_team_stats["player_stats"][name]["player_id"] = id
            
            away_team_stats = {
                'team_name' : f'{df["awayTeam"]["teamCity"]} {df["awayTeam"]["teamName"]}',
                'team_id' : df["awayTeam"]["teamId"],
                'points' : df["awayTeam"]["statistics"]["points"],
                'field_goals_made' : df["awayTeam"]["statistics"]["fieldGoalsMade"],
                'field_goals_attempted' : df["awayTeam"]["statistics"]["fieldGoalsAttempted"],
                'field_goal_percentage' : df["awayTeam"]["statistics"]["fieldGoalsPercentage"],
                'three_pointers_made' : df["awayTeam"]["statistics"]["threePointersMade"],
                'three_pointers_attempted' : df["awayTeam"]["statistics"]["threePointersAttempted"],
                'three_pointers_percentage' : df["awayTeam"]["statistics"]["threePointersPercentage"],
                'free_throws_made' : df["awayTeam"]["statistics"]["freeThrowsMade"],
                'free_throws_attempted' : df["awayTeam"]["statistics"]["freeThrowsAttempted"],
                'free_throws_percentage' : df["awayTeam"]["statistics"]["freeThrowsPercentage"],
                'rebounds' : df["awayTeam"]["statistics"]["reboundsTotal"],
                'assists' : df["awayTeam"]["statistics"]["assists"],
                'steals' : df["awayTeam"]["statistics"]["steals"],
                'blocks' : df["awayTeam"]["statistics"]["blocks"],
                'turnovers' : df["awayTeam"]["statistics"]["turnovers"],
                'player_stats' : {}
            }

            for player in df["awayTeam"]["players"]:
                id = player["personId"]
                name = f'{player["firstName"]} {player["familyName"]}'
                away_team_stats["player_stats"][name] = player["statistics"]
                # add the players id to the dictionary
                away_team_stats["player_stats"][name]["player_id"] = id

            # map game id to its relevant statistics
            self.game_ids[id_key] = {'home_team_stats' : home_team_stats, 'away_team_stats' : away_team_stats}

    
    def rank_players_for_game(self):
        # for testing, extract the id of the first game and store in a variable 
        for id_key in self.game_ids:
            player_game_scores = []
            for player in self.game_ids[id_key]['home_team_stats']['player_stats']:
                score = 0.0
                for stat in self.player_performance_weights:
                    score += (self.game_ids[id_key]['home_team_stats']['player_stats'][player][stat] * self.player_performance_weights[stat])
                
                player_game_scores.append((score, player))
            
            player_game_scores.sort()
            # delete all the player statistics except the 2 highest performers 
            i = 0
            for score, player in player_game_scores:
                # if we are on one of the two highest performers, keep their game information 
                if i >= len(player_game_scores) - 2:
                    continue
                # delete all other players stats to save token consumption
                del self.game_ids[id_key]['home_team_stats']['player_stats'][player]
                i += 1

            player_game_scores = []
            for player in self.game_ids[id_key]['away_team_stats']['player_stats']:
                score = 0.0
                for stat in self.player_performance_weights:
                    score += (self.game_ids[id_key]['away_team_stats']['player_stats'][player][stat] * self.player_performance_weights[stat])
                
                player_game_scores.append((score, player))
            
            player_game_scores.sort()
            # delete all the player statistics except the 2 highest performers 
            i = 0
            for score, player in player_game_scores:
                # if we are on one of the two highest performers, keep their game information 
                if i >= len(player_game_scores) - 2:
                    continue
                # delete all other players stats to save token consumption
                del self.game_ids[id_key]['away_team_stats']['player_stats'][player]
                i += 1

    def generate_game_summary(self):
        for id_key in self.game_ids:
            self.messages.append({
                "role" : "user",
                "content" : str(self.game_ids[id_key])
            })

            # send a request to the model 
            chat_completion = self.client.chat.completions.create(
                messages = self.messages,
                model = self.model,
                temperature = 0.35
            )

            # capture the classification
            summary = chat_completion.choices[0].message.content
            # pop the query from the message history
            self.messages.pop()
            self.game_summaries[id_key] = summary

    def write_team_snapshots(self):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)
        
        # loop through each team and take a snapshot of their common info, including wins, losses, and conference standing
        for team in CommonLeagueInfo.TEAM_IDS:
            df = nba_api.TeamInfoCommon(team).get_data_frames()[0]
            # need to handle some explicity type casting from numpy 64-bit ints and floats
            database_fields_map = {
                "team_id" : int(df["TEAM_ID"].values[0]),
                "season" : df["SEASON_YEAR"].values[0],
                "city" : df["TEAM_CITY"].values[0],
                "team_name" : df["TEAM_NAME"].values[0],
                "conference" : df["TEAM_CONFERENCE"].values[0],
                "division" : df["TEAM_DIVISION"].values[0],
                "wins" : int(df["W"].values[0]),
                "losses" : int(df["L"].values[0]),
                "win_pct" : float(df["PCT"].values[0]),
                "conference_standing" : int(df["CONF_RANK"].values[0]),
                "date" : self.date
            }
            
            response = self.supabase.table("Team Snapshots").insert(database_fields_map).execute()
            print(response)

            # avoid repeatedly spamming the API which was causing some blocking issues by sleeping the process for a second
            time.sleep(1)
            
    def user_authentication_email(self, email: str, password: str):
        response = self.supabase.auth.sign_in_with_password(
            {
                "email" : email,
                "password" : password
            }
        )

        return response
            
    def write_summaries(self):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        for id_key in self.game_summaries:
            # need to write some regex to extract each key part of a summary out
            pattern = re.compile(r"(?s)SCORE\s*(.*?)\s*DETAILS\s*(.*?)\s*KEY PERFORMERS\s*(.*)")

            match = pattern.search(self.game_summaries[id_key])

            if match:
                score = match.group(1).strip()
                details = match.group(2).strip()
                key_performers = match.group(3).strip()
                key_performers = key_performers.split("\n")
                key_performers = [item.strip() for item in key_performers if item.strip()]
                database_fields_map = {
                    'game_id' : id_key,
                    'home_team_id' : self.game_ids[id_key]['home_team_stats']['team_id'],
                    'away_team_id' : self.game_ids[id_key]['away_team_stats']['team_id'],
                    'headline' : score,
                    'game_description' : details,
                    'key_player_ids' : [],
                    'key_player_descriptions' : key_performers,
                    'date' : self.date
                }

                # add player ids to database object
                for player in self.game_ids[id_key]['home_team_stats']['player_stats']:
                    database_fields_map['key_player_ids'].append(self.game_ids[id_key]['home_team_stats']['player_stats'][player]['player_id'])
                for player in self.game_ids[id_key]['away_team_stats']['player_stats']:
                    database_fields_map['key_player_ids'].append(self.game_ids[id_key]['away_team_stats']['player_stats'][player]['player_id'])

                response = self.supabase.table("Summaries").insert(database_fields_map).execute()
                print(response)
            else:
                print(f'Error generating summary, see details:\n{self.game_summaries[id_key]}')

    def write_standings(self):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        database_fields_map = {
            "date" : self.date,
            "east_rankings" : self.east_standings,
            "west_rankings" : self.west_standings
        }

        response = self.supabase.table("Standings").insert(database_fields_map).execute()
        print(response)