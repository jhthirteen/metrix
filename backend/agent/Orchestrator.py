import autogen
from agent_config import llm_config

# importing all agents
from Identity import boot_identity_agent
from LeagueLeaders import boot_league_leaders_agent

# importing all tools
from identity_tools import get_player_ids, get_team_ids, get_common_player_info, get_common_team_roster, get_common_team_coaching, search_player_index_history, search_player_index_season, get_common_team_info_season, get_team_history
from league_leaders_tools import get_all_time_leader, get_team_stat_leader, get_league_standings_season, get_stat_leader_averages_season, get_stat_leader_totals_season

# init and config of tool executor 
admin_executor = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    code_execution_config={"work_dir" : "coding", "use_docker" : False},
    is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or "")
)
identity_agent = boot_identity_agent()
league_leaders_agent = boot_league_leaders_agent()

# register all the identity tools
autogen.register_function(
    get_player_ids,
    caller=identity_agent,
    executor=admin_executor,
    name="get_player_ids",
    description="Search for a players id based on their name."
)

autogen.register_function(
    get_team_ids,
    caller=identity_agent,
    executor=admin_executor,
    name="get_team_ids",
    description="Search for a teams id based on their name."
)

autogen.register_function(
    get_common_player_info,
    caller=identity_agent,
    executor=admin_executor,
    name="get_common_player_info",
    description="Get common info based on a players id. Includes: biographical, school, physical, team, and draft information"
)

autogen.register_function(
    search_player_index_season,
    caller=identity_agent,
    executor=admin_executor,
    name="search_player_index_season",
    description="Filter out to find all players in a season that meet some search criteria: school, draft info, country, physical, team, or jersey."
)

autogen.register_function(
    search_player_index_history,
    caller=identity_agent,
    executor=admin_executor,
    name="search_player_index_history",
    description="Filter out to find all players historically that meet some search criteria: school, draft info, country, physical, team, or jersey."
)

autogen.register_function(
    get_common_team_roster,
    caller=identity_agent,
    executor=admin_executor,
    name="get_common_team_roster",
    description="Get the players on a teams roster for a specific season"
)

autogen.register_function(
    get_common_team_coaching,
    caller=identity_agent,
    executor=admin_executor,
    name="get_common_team_coaching",
    description="Get a teams coaching staff information for a specific season"
)

autogen.register_function(
    get_common_team_info_season,
    caller=identity_agent,
    executor=admin_executor,
    name="get_common_team_info_season",
    description="Get information for a team for a specific season, including: the team's city, name, conference, division, wins, losses, and standings"
)

autogen.register_function(
    get_team_history,
    caller=identity_agent,
    executor=admin_executor,
    name="get_team_history",
    description="Get the history for a team, including: management, team awards, hall of famers, and retired players"
)

# register all the league leaders tool calls
autogen.register_function(
    get_team_ids,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_team_ids",
    description="Search for a teams id based on their name."
)

autogen.register_function(
    get_all_time_leader,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_all_time_leader",
    description="Search for the all-time NBA leader for a stat"
)

autogen.register_function(
    get_team_stat_leader,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_team_stat_leader",
    description="Search for the stat leader for a specific team"
)

autogen.register_function(
    get_league_standings_season,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_league_standings_season",
    description="Search for the NBA standings for a specific season"
)

autogen.register_function(
    get_stat_leader_averages_season,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_stat_leader_averages_season",
    description="Search for the stat leader per game for a specific season"
)

autogen.register_function(
    get_stat_leader_totals_season,
    caller=league_leaders_agent,
    executor=admin_executor,
    name="get_stat_leader_totals_season",
    description="Search for the stat leader totals for a specific season"
)

#workspace = autogen.GroupChat(
    #agents=[admin_executor, identity_agent],
    #messages=[],
    #max_round=15
#)

#manager = autogen.GroupChatManager(groupchat=workspace, llm_config=llm_config)

admin_executor.initiate_chat(
    league_leaders_agent,
    message="Who is leading the NBA in points per game this season?"
)