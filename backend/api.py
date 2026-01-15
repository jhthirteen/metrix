from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Classifier import Classifier
from PlayerCard import PlayerCard
from ToolInterface import ToolInterface
from datetime import date
from Newsletter import Newsletter

app = FastAPI()
classifier = Classifier()
tools = ToolInterface()

# setup middleware to allow requests coming from the dev environment
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryBody(BaseModel):
    q: str
 
 # TODO: add a NameParser object here to extract the names relevant to the request --> add to the return object 
@app.post("/query")
def query(user_query: QueryBody):
    query_type = classifier.classify_query(user_query.q)
     # TODO: add some kind of logging mechanism here so that we can easily investigate why querires are failing 
    if( query_type not in {"Player", "Team", "PlayerComparison", "TeamComparison", "PlayerFetch", "TeamFetch"} ):
        raise HTTPException(status_code=422, detail="Server classification failure. Please try again later")
    
    return {"query_type" : query_type}


@app.get("/playercard")
def playercard(player_name: str):
    # check that player name is non-empty 
    if( not player_name ):
        raise HTTPException(status_code=400, detail="Empty request")

    player_card = PlayerCard(player_name)
    return player_card.build_player_card()

class ToolBody(BaseModel):
    q: str
    q_type: str

@app.post("/usetool")
def usetool(user_query: ToolBody):
    if( user_query.q_type == "Player" ):
        answer = tools.run_tool(user_query.q)
    else:
        answer = {"raw_stat" : 0, "stat_formatted" : "Null"}
    
    return answer


@app.get("/fetchsummaries")
def fetchsummaries(games_date: str):
    summary_generator = Newsletter()
    # handle the collection of summaries, news articles, highlights, and standings updates
    summaries = summary_generator.fetch_summaries(games_date)
    news = summary_generator.fetch_news(games_date)
    highlights = summary_generator.fetch_highlights(games_date)
    standings = summary_generator.fetch_standings_changes()
    return {"summaries" : summaries, "news" : news, "highlights" : highlights, "standings" : standings}