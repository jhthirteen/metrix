from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# encapsulating possible context values that could be needed to execute a query
class QueryContext(BaseModel):
    player_id: Optional[int] = None
    player_name: Optional[str] = None
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    game_id: Optional[int] = None
    season: Optional[str] = None
    to_date: Optional[str] = None
    from_date: Optional[str] = None

class AgentWorkspace(BaseModel):
    # passing the message history between agents. default_factory ensures a NEW object is created every time
    message_history: List[Dict[str, str]] = Field(default_factory=list)
    context: QueryContext = Field(default_factory=QueryContext)

    # traversal logic 
    step_intent: Optional[str] = None
    next_agent: Optional[str] = None

    # space for us to store and work with the results of existing tool-calls. Map agent called --> result
    toolcall_results: Optional[Dict[str, Any]] = None