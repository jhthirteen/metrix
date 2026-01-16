import identity_tools
import inspect 
import nba_api.stats.endpoints as nba_api
import league_leaders_tools
import box_score_tools

#t = league_leaders_tools.get_all_time_leader(league_leaders_tools.AllTimeStat.points, 25)
#z = league_leaders_tools.get_team_stat_leader(1610612742, [league_leaders_tools.FranchiseLeaderStat.points, league_leaders_tools.FranchiseLeaderStat.steals])

bs = box_score_tools.get_game_box_score(game_id='0022300061')
print(bs)