from PlayerCard import PlayerCard

class QueryResponse:
    def __init__(self, query_type: str, tool_used: str, response: str, search_item: str):
        self.query_type = query_type
        self.tool_used = tool_used
        self.response = response
        self.search_item = search_item

        self.player_responses = {}
    
    def return_player_response(self, player: str, stat: str, stat_val: str):
        pass