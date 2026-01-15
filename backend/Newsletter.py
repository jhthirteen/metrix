from nba_api.stats.static import players
import nba_api.stats.endpoints as nba_api
from datetime import date, timedelta, datetime
import os
from groq import Groq
from supabase import Client, create_client
import re

class Newsletter:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)
        self.summaries = []
        self.news = []
        self.highlights = []
        self.eastern_conference_deltas = {}
        self.western_conference_deltas = {}

    def user_authentication_email(self, email: str, password: str):
        response = self.supabase.auth.sign_in_with_password(
            {
                "email" : email,
                "password" : password
            }
        )

        return response
            
    def fetch_summaries(self, date: str):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        
        response = (
            self.supabase.table("Summaries")
            .select("*")
            .eq("date", date)
            .execute()
        )

        self.summaries = response.data
        return self.summaries
    
    def fetch_news(self, date: str):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        
        response = (
            self.supabase.table("News")
            .select("*")
            .eq("date", date)
            .execute()
        )

        self.news = response.data
        return self.news

    def fetch_highlights(self, date: str):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        
        response = (
            self.supabase.table("Highlights")
            .select("*")
            .eq("date", date)
            .execute()
        )

        self.highlights = response.data
        return self.highlights

    def fetch_standings_changes(self):
        # HARDCODE AUTH IN FOR NOW
        user = os.getenv('SUPABASE_ROOT_USER')
        passw = os.getenv('SUPABASE_ROOT_PW')

        # try to authenticate to write to the database
        try:
            auth = self.user_authentication_email(user, passw)
        except Exception as e:
            print(e)

        # can we enacpsulate this into a single database call?? probably

        response = (
            self.supabase.table("Standings")
            .select("*")
            .execute()
        )

        back = len(response.data) - 1

        current_standings = response.data[back]
        prev_standings = response.data[back-1]

        # calculate the delta in standing positions from prev --> current

        # map each teams id to their positions in the standings from the previous day
        for i in range(len(prev_standings['east_rankings'])):
            team_id = prev_standings['east_rankings'][i]
            self.eastern_conference_deltas[team_id] = i + 1

        for i in range(len(prev_standings['west_rankings'])):
            team_id = prev_standings['west_rankings'][i]
            self.western_conference_deltas[team_id] = i + 1
        
        # now, calculate the change from their position in the current standings
        for i in range(len(current_standings['east_rankings'])):
            team_id = current_standings['east_rankings'][i]
            self.eastern_conference_deltas[team_id] = [self.eastern_conference_deltas[team_id] - (i + 1), i + 1]
        
        for i in range(len(current_standings['west_rankings'])):
            team_id = current_standings['west_rankings'][i]
            self.western_conference_deltas[team_id] = [self.western_conference_deltas[team_id] - (i + 1), i + 1]

        # final data is a map of the form team id --> [change in standings, cur position in standings]
        return {
            "western_conference_deltas" : self.western_conference_deltas,
            "eastern_conference_deltas" : self.eastern_conference_deltas
        }
#TODO: clean this up once the database module is written