from PlayerTools import PlayerTools

class PlayerCard:
    def __init__(self, player_name: str):
        # initialize the tool interface and fetch the player id to search for specific information 
        self.tools = PlayerTools()
        self.player_name = player_name
        self.id = self.tools.get_player_id(self.player_name)

        # plug player id into NBA image URL base
        self.player_image_url = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{self.id}.png'

        # TODO: implement self.image        
        # fetch the player info for the card banner 
        self.team = self.tools.get_player_team(self.id, self.player_name)["raw_stat"]
        self.position = self.tools.get_player_position(self.id, self.player_name)["raw_stat"]
        self.jersey_number = self.tools.get_player_jersey_number(self.id, self.player_name)["raw_stat"]
        self.jersey_number = '#' + self.jersey_number

        # fetch awards for award section
        self.awards = self.tools.get_player_awards(self.id)

        # fetch career statistics for stats section
        self.career_stats = self.tools.get_player_career_stats_totals(self.id)
        
    def build_player_card(self):
        games_played = self.career_stats["GP"].item()
        # calculate career points per game
        ppg = self.career_stats["PTS"].item() / games_played
        ppg = str(round(ppg, 1))
        # calculate career rebounds per game
        rpg = self.career_stats["REB"].item() / games_played
        rpg = str(round(rpg, 1))
        # calculate career assists per game
        apg = self.career_stats["AST"].item() / games_played
        apg = str(round(apg, 1))
        # calculate career field goal percentage
        fgpct = self.career_stats["FG_PCT"].item() * 100
        fgpct = str(round(fgpct, 2))
        # calculate career steals per game
        spg = self.career_stats["STL"].item() / games_played
        spg = str(round(spg, 1))
        # calculate career blocks per game
        bpg = self.career_stats["BLK"].item() / games_played
        bpg = str(round(bpg, 1))

        return {
            "NAME" : self.player_name,
            "TEAM" : self.team,
            "POSITION" : self.position,
            "JERSEY" : self.jersey_number,
            "PPG" : ppg,
            "APG" : apg,
            "FG" : fgpct,
            "RPG" : rpg,
            "SPG" : spg,
            "BPG" : bpg,
            "AWARDS" : self.awards,
            "IMG" : self.player_image_url
        }
    
    def get_player_image(self):
        return self.player_image_url