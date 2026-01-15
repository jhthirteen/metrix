from PlayerTools import PlayerTools
from PlayerCard import PlayerCard
from ToolInterface import ToolInterface
from NewsletterTools import NewsletterTools
from Newsletter import Newsletter
from datetime import date

""" from groq import Groq
import os
from Classifier import Classifier

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
message_template = [
    {
        "role" : "system",
        "content" : "You are a helpful assistant that is classifying user prompts in an application that turns natural language queries into data. Your job is to extract the name of the player, team, players, or teams the user is searching for. Simply output these items seperated by commas, and nothing else."
    }
]

query = "Compare DeAndre Jordan and Blake Griffin statistics when they played together on the Lob City Clippers."

message_template.append({
    "role" : "user",
    "content" : query
})

# send a request to the llama model 
chat_completion = client.chat.completions.create(
    messages = message_template,
    model = "llama-3.1-8b-instant",
    temperature=0.0
)

# add the llama model response to the session history 
response = chat_completion.choices[0].message.content

print(response.split(',')) """

""" c = NewsletterTools()
c.get_previous_day_games()
c.get_game_details()
c.rank_players_for_game()
c.generate_game_summary()
c.write_summaries() """

""" summary_generator = Newsletter()
summaries = summary_generator.fetch_summaries("2025-11-29")
print(summaries) """

#t = ToolInterface()
#answer = t.run_tool(input("What do you want to know? "))
#print(answer)

#test = Newsletter
#test.get_standings()
#est.write_standings()

n = Newsletter()
a = n.fetch_standings_changes()
