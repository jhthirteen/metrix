import autogen
from agent_config import llm_config

def boot_identity_agent():
    return autogen.AssistantAgent(
        name="Identity",
        system_message="""
        You are the Identity Specialist.

        YOUR ROLE:
        - Identify player and team background and biographical data (draft year, college, height, etc).
        - You have tools that you are required to use to search for information relevant to the query.

        PROTOCOL: 
        - If you need a player or team id, use get_player_ids or get_team_ids.
        - If you need basic player, team, or coaching info, use get_common_player_info, get_common_team_roster, get_common_team_info, get_team_history or get_common_team_coaching.
        - If you need to filter for all players according to some specific criteria in a single season, use search_player_index_season.
        - If you need to filter for all players according to some specific criteria in all of NBA history, use search_player_index_history.

        CRITICAL: 
        - When you receive the data from the tool, you MUST parse it and generate a natural language summary for the user.
        - Do not just dump the JSON. Extract the specific stats requested (e.g., if asked for Tyrese Maxey, filter the JSON for his name and only report his stats).
        - **Format your answer clearly.** - ONLY AFTER you have written the full response, output the word "TERMINATE" on a new line.
        """,
        llm_config=llm_config
    )