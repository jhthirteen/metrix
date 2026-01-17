import identity_tools
import inspect 
import nba_api.stats.endpoints as nba_api
import league_leaders_tools
import box_score_tools

#t = league_leaders_tools.get_all_time_leader(league_leaders_tools.AllTimeStat.points, 25)
#z = league_leaders_tools.get_team_stat_leader(1610612742, [league_leaders_tools.FranchiseLeaderStat.points, league_leaders_tools.FranchiseLeaderStat.steals])

t = identity_tools.search_player_index_history(college="Syracuse", draft_pick=1, draft_round=1)
print(t)