from nba_api.stats.static import players
import nba_api.stats.endpoints as nba_api

class PlayerTools:
    def __init__(self):
        self.base_url = "https://stats.nba.com/stats/"

    def get_player_id(self, player_name: str) -> int:
        # assumes that there should be a single match to this name 
        res = players.find_players_by_full_name(player_name)
        # if the query resulted in no matches, throw an error
        if( not res ):
            raise ValueError("Player does not exist")
        
        return res[0]['id']
    
    def get_common_player_info_item(self, player_id: int, item: str) -> str:
        # make API request to resource
        response = nba_api.CommonPlayerInfo(player_id)
        # extract response as a dataframe 
        df = response.get_data_frames()

        return df[0][item].item()
    
    def get_player_awards(self, player_id: int) -> dict[str, int]:
        # make API request to resource
        response = nba_api.PlayerAwards(player_id)
        # extract response as a dataframe
        df = response.get_data_frames()
        df = df[0]["DESCRIPTION"]
        # build out awards dictionary 
        awards_count = {}

        for award in df:
            # check if the award has been previously seen or not 
            if( award not in awards_count ):
                awards_count[award] = 0
            awards_count[award] += 1

        return awards_count
    
    def get_player_career_stats_profile(self, player_id: int):
        # make API request to resource
        response = nba_api.PlayerCareerStats(player_id)
        # extract responses as a dataframe
        df = response.get_data_frames()
        return df[0]
    
    def get_player_career_stats_totals(self, player_id: int):
        # make API request to resource
        response = nba_api.PlayerCareerStats(player_id)
        # extract responses as a dataframe
        df = response.get_data_frames()
        return df[1]
    
    def get_player_shot_chart_details_for_year(self, player_id: int, year: str) -> str:
        # make API request to resource
        response = nba_api.PlayerDashPtShots(player_id=player_id, season=year, team_id=0)
        # extract responses as a datafrmae
        df = response.get_data_frames()
        return df[0]
    
    def get_player_heatmap_for_year(self, player_id: int, year: str) -> str:
        # make API request to resource. Note: context_measure_simple="FGA" paramater gives us all shot attempts (makes and misses)
        response = nba_api.ShotChartDetail(player_id=player_id, season_nullable=year, team_id=0, context_measure_simple="FGA")
        # extract responses as a dataframe
        df = response.get_data_frames()
        return df[0]

    def get_player_fg_pct_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        fg_pct = df[df["SEASON_ID"] == year]["FG_PCT"].item()
        formatted_str = f'{player_name} shot [b]{fg_pct}[/b] from the field in the {year} season.'
        return {"raw_stat" : fg_pct, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_3pt_pct_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        three_pt_pct = df[df["SEASON_ID"] == year]["FG3_PCT"].item()
        formatted_str = f'{player_name} shot [b]{three_pt_pct}[/b] from three in the {year} season.'
        return {"raw_stat" : three_pt_pct, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_ft_pct_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        ft_pct = df[df["SEASON_ID"] == year]["FT_PCT"].item()
        formatted_str = f'{player_name} shot [b]{ft_pct}[/b] from the free throw line in the {year} season.'
        return {"raw_stat" : ft_pct, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_rebounds_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        reb = df[df["SEASON_ID"] == year]["REB"].item()
        formatted_str = f'{player_name} had [b]{reb}[/b] rebounds in the {year} season.'
        return {"raw_stat" : reb, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_assists_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        ast = df[df["SEASON_ID"] == year]["AST"].item()
        formatted_str = f'{player_name} had [b]{ast}[/b] assists in the {year} season.'
        return {"raw_stat" : ast, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_steals_for_year(self, player_id: int, year: str, player_name: str) -> str: 
        df = self.get_player_career_stats_profile(player_id)
        stl = df[df["SEASON_ID"] == year]["STL"].item()
        formatted_str = f'{player_name} had [b]{stl}[/b] steals in the {year} season.'
        return {"raw_stat" : stl, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_blocks_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        blk = df[df["SEASON_ID"] == year]["BLK"].item()
        formatted_str = f'{player_name} had [b]{blk}[/b] blocks in the {year} season.'
        return {"raw_stat" : blk, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_turnovers_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        tov = df[df["SEASON_ID"] == year]["TOV"].item()
        formatted_str = f'{player_name} had [b]{tov}[/b] turnovers in the {year} season.'
        return {"raw_stat" : tov, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_points_for_year(self, player_id: int, year: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        pts = df[df["SEASON_ID"] == year]["PTS"].item()
        formatted_str = f'{player_name} had [b]{pts}[/b] points in the {year} season.'
        return {"raw_stat" : pts, "stat_formatted" : formatted_str, "player_name" : player_name}
    
    def get_player_stat_average_per_game_for_year(self, player_id: int, year: str, stat: str, player_name: str) -> str:
        df = self.get_player_career_stats_profile(player_id)
        season_row = df[df["SEASON_ID"] == year]
        stat_average_per_game = season_row[stat].item() / season_row["GP"].item() 
        stat_average_per_game = round(stat_average_per_game, 1)

        stat_formatted = {'PTS' : 'points', 'REB' : 'rebounds', 'AST' : 'assists', 'STL' : 'steals', 'BLK' : 'blocks', 'TOV' : 'turnovers'}
        formatted_str = f'{player_name} averaged [b]{stat_average_per_game}[/b] {stat_formatted[stat]} in the {year} season.'

        visual_data = self.get_player_points_visuals_for_year(player_id, year)

        return {"raw_stat" : stat_average_per_game, "stat_formatted" : formatted_str, "player_name" : player_name, "visuals" : visual_data}

    def get_player_college(self, player_id: int, player_name: str) -> str:
        college = self.get_common_player_info_item(player_id, "SCHOOL")
        formatted_str = f'{player_name} attended [b]{college}.[/b]'
        return {"raw_stat" : college, "stat_formatted" : formatted_str}
    
    def get_player_height(self, player_id: int, player_name: str) -> str:
        height =  self.get_common_player_info_item(player_id, "HEIGHT")
        formatted_str = f'{player_name} is [b]{height}[/b] tall.'
        return {"raw_stat" : height, "stat_formatted" : formatted_str}

    def get_player_weight(self, player_id: int, player_name: str) -> str:
        weight = self.get_common_player_info_item(player_id, "WEIGHT")
        formatted_str = f'{player_name} weight [b]{weight}[/b] pounds.'
        return {"raw_stat" : weight, "stat_formatted" : formatted_str}
    
    def get_player_team(self, player_id: int, player_name: str) -> str:
        team = self.get_common_player_info_item(player_id, "TEAM_NAME")
        formatted_str = f'{player_name} plays for the [b]{team}.[/b]'
        return {"raw_stat" : team, "stat_formatted" : formatted_str}
    
    def get_player_jersey_number(self, player_id: int, player_name: str) -> str:
        jersey_num = self.get_common_player_info_item(player_id, "JERSEY")
        formatted_str = f'{player_name} wears jersey number [b]{jersey_num}.[/b]'
        return {"raw_stat" : jersey_num, "stat_formatted" : formatted_str}
    
    def get_player_position(self, player_id: int, player_name: str) -> str:
        position = self.get_common_player_info_item(player_id, "POSITION")
        formatted_str = f'{player_name} is a [b]{position}.[/b]'
        return {"raw_stat" : position, "stat_formatted" : formatted_str}
    
    def get_player_image(self, player_id: int) -> str:
        return f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
    
    def get_player_points_visuals_for_year(self, player_id: int, year: str):
        '''
        1) show how this compares to their career scoring average
        2) show how the breakdown for the particular year is (shot diet, mid range, three, close)
        3) show how it compares to similar players! (implement last)
        '''
        charts = []
        # getting average numbers for each season
        df = self.get_player_career_stats_profile(player_id)
        season_averages = [0] * len(df)
        for index, row in df.iterrows():
            ppg = row["PTS"] / row["GP"]
            ppg = round(ppg, 2)
            season = str(row["SEASON_ID"])
            color = 0
            if( year == season ):
                color = 1
            season_averages[index] = {'name' : season, 'value' : ppg, 'color' : color}
    
        charts.append({'chart_type' : 'bar', 'chart_data' : season_averages})
        # getting the players shot diet for the given year
        df = self.get_player_shot_chart_details_for_year(player_id, year)
        shot_diet = [0] * 2
        shot_diet[0] = {'name' : '2PT Frequency', 'value' : df['FG2A_FREQUENCY'].item()}
        shot_diet[1] = {'name' : '3PT Frequency', 'value' : df['FG3A_FREQUENCY'].item()}

        charts.append({'chart_type' : 'pie', 'chart_data' : shot_diet})

        # building a heat map for a players scoring for the given season
        df = self.get_player_heatmap_for_year(player_id, year)
        heatmap = [0] * len(df)
        for index, row in df.iterrows():
            x = row["LOC_X"]
            y = row["LOC_Y"]
            made = row["SHOT_MADE_FLAG"]
            heatmap[index] = (x, y, made)

        return charts




# IDEAS
# one idea is we can pull all the common player info to build some kind of player "card",
# so, whenever someone searches for stats on a player, they can link to a specific card UI screen that shows more!