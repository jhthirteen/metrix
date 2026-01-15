from PlayerTools import PlayerTools
import os
from groq import Groq
import json 

class ToolInterface:
    def __init__(self):

        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.message_template = [
            {
                "role" : "system",
                "content" : "Your job is to match the given user query to the tool that best accomplishes what the user is searching for"
            }
        ]
        self.model = "openai/gpt-oss-20b"

        #TODO: can we automate the accumulation of these functions / descriptions? making it all dynamic would be a lot easier
        self.player_toolkit = PlayerTools()
        
        self.tools = [
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_awards",
                    "description" : "returns a dictionary of all the NBA Awards a player has won in their career",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"}
                        },
                        "required" : ["player_name"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_fg_pct_for_year",
                    "description" : "returns a players field goal percentage for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_3pt_pct_for_year",
                    "description" : "returns a players three point percentage for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },   
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_ft_pct_for_year",
                    "description" : "returns a players free throw percentage for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_rebounds_for_year",
                    "description" : "returns a players total rebounds for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_assists_for_year",
                    "description" : "returns a players total assists for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_steals_for_year",
                    "description" : "returns a players total steals for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_blocks_for_year",
                    "description" : "returns a players total blocks for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_turnovers_for_year",
                    "description" : "returns a players total turnovers for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },  
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_points_for_year",
                    "description" : "returns a players total points for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            },
            {
                "type" : "function",
                "function" : {
                    "name" : "get_player_stat_average_per_game_for_year",
                    "description" : "returns the average of a user specified stat per game for a given year",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "player_name" : {"type" : "string", "description" : "should always be a players full first and last name"},
                            "year" : {"type" : "string", "description" : "Season year in the format YYYY-YY (e.g., 2020-21 for the 2020 to 2021 season)."},
                            "stat" : {"type" : "string", "description" : "Must be one of the following: PTS, REB, AST, STL, BLK, TOV "}
                        },
                        "required" : ["player_name", "year"]
                    }
                }
            }         
        ]

        self.player_tool_functions = {
            "get_player_awards" : self.player_toolkit.get_player_awards,
            "get_player_fg_pct_for_year" : self.player_toolkit.get_player_fg_pct_for_year,
            "get_player_3pt_pct_for_year" : self.player_toolkit.get_player_3pt_pct_for_year,
            "get_player_ft_pct_for_year" : self.player_toolkit.get_player_ft_pct_for_year,
            "get_player_rebounds_for_year" : self.player_toolkit.get_player_rebounds_for_year,
            "get_player_assists_for_year" : self.player_toolkit.get_player_assists_for_year,
            "get_player_steals_for_year" : self.player_toolkit.get_player_steals_for_year,
            "get_player_blocks_for_year" : self.player_toolkit.get_player_blocks_for_year,
            "get_player_turnovers_for_year" : self.player_toolkit.get_player_turnovers_for_year,
            "get_player_points_for_year" : self.player_toolkit.get_player_points_for_year,
            "get_player_stat_average_per_game_for_year" : self.player_toolkit.get_player_stat_average_per_game_for_year
        }

    def select_player_tool(self, q: str):
        # add the user query to the classifier message history
        self.message_template.append({
            "role" : "system",
            "content" : q
        })

        # send a request to the model 
        chat_completion = self.client.chat.completions.create(
            messages = self.message_template,
            model = self.model,
            tools = self.tools,
            tool_choice = "auto"
        )

        # capture the correct tool to use
        tool = chat_completion.choices[0].message
        
        # pop the query from the message history
        self.message_template.pop()

        tool_name = tool.tool_calls[0].function.name
        tool_args = tool.tool_calls[0].function.arguments
        
        # we want to replace the player name arg with player id
        tool_args = json.loads(tool_args)
        tool_args["player_id"] = self.player_toolkit.get_player_id(tool_args["player_name"])

        player_image_url = self.player_toolkit.get_player_image(tool_args["player_id"])

        return {"tool_name" : tool_name, "tool_args" : tool_args, "player_image" : player_image_url}
    
    def run_tool(self, q: str):
        tool_call_info = self.select_player_tool(q)

        func_name = tool_call_info["tool_name"]
        func_args = tool_call_info["tool_args"]
        player_image = tool_call_info["player_image"]

        # find the function pointer in to the correct tool 
        func = self.player_tool_functions[func_name]
        
        # unpack the dictionary args and pass them into the function 
        query_stats = func(**func_args)

        query_stats["player_image"] = player_image

        return query_stats