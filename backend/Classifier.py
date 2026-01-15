import os
from groq import Groq

class Classifier:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.message_template = [
            {
                "role" : "system",
                "content" : "You are a helpful assistant that is classifying user prompts in an application that turns natural language queries into data. There are 6 possible query groupings: Player, Team, PlayerComparison, TeamComparison, PlayerFetch, TeamFetch. Please output the group of the query, and ONLY the group of the query. Player is when the user is searching something related to a single player, Team is when the user is searching something related to a single team, PlayerComparison is when the user is searching something related to 2 or more players, TeamComparison is when the user is searching something related to 2 or more teams. PlayerFetch is when the user is searching for players that fit some specific criteria. TeamFetch is when the user is searching for teams that fit some specific criteria."
            }
        ]
        self.model = "openai/gpt-oss-20b"

    def classify_query(self, q: str) -> str:
        # add the user query to the classifier message history
        self.message_template.append({
            "role" : "user",
            "content" : q
        })

        # send a request to the model 
        chat_completion = self.client.chat.completions.create(
            messages = self.message_template,
            model = self.model,
            temperature = 0.0
        )

        # capture the classification
        classification = chat_completion.choices[0].message.content

        # pop the query from the message history
        self.message_template.pop()

        return classification