import requests
import os
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import re
from supabase import Client, create_client
from datetime import date

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
message_template_news = [
    {
        "role" : "system",
        "content" : """You are an expert NBA Analyst that is summarizing news stories from the NBA Subreddit. You will be fed one or more posts that have a similar underlying story, and should be combined into a single news story that summarizes all the input posts. Please use exactly the following format: {{Headline: output_headline, Story: output_story}}. You are required to use the words Headline and Story, do not use other words in the JSON. Do not come up with, or include any additional information that is not present in the input. Don't add additional quotations or anything to the output either."""
    }
]

message_template_highlight = [
    {
        "role" : "system",
        "content" : "You are an expert NBA Analyst. You will be presented with the name of a highlight from the NBA, your task is to word it in a way that is professional, and clean of any language that is inappropriate or meme-like. Simply output the new highlight title, and nothing else."
    }
]

model = "openai/gpt-oss-120b"

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def summarize_news_story(post: str) -> str:
    # add the user query to the classifier message history
    message_template_news.append({
        "role" : "user",
        "content" : post
    })

    # send a request to the model 
    chat_completion = client.chat.completions.create(
        messages = message_template_news,
        model = model,
        temperature = 0.5
    )

    # capture the classification
    classification = chat_completion.choices[0].message.content

    # pop the query from the message history
    message_template_news.pop()

    return classification

def summarize_highlight(post: str) -> str:
    # add the highlight name to the message history
    message_template_highlight.append({
        "role" : "user",
        "content" : post
    })

    # send a request to the model
    chat_completion = client.chat.completions.create(
        messages = message_template_highlight,
        model = model,
        temperature = 0.5
    )

    highlight_name = chat_completion.choices[0].message.content
    message_template_highlight.pop()
    
    return highlight_name

def reddit_pipeline():
    url = "https://www.reddit.com/r/nba/best/.json?t=day"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    data = data['data']['children']

    # handle case where we get an empty json object
    if not data:
        raise Exception("Data Request down at this time... please try again later")

    batch_stories = []
    post_headlines = []
    post_text = []
    post_media = []
    i = 0
    #NOTE: it may be more efficient / cleaner here to use an index based dictionary that maps to all relevant post info, rather than independent ararys 
    for highlight in data:
        headline = highlight['data']['title']
        text = highlight['data']['selftext_html']
        # case: we have large HTML box-scores embedded in the post --> remove this information 
        if text and len(text) > 500:
            text = None
        
        media = None
        if 'url_overridden_by_dest' in highlight['data']:
            media = highlight['data']['url_overridden_by_dest']

        # store the post name & matching index in a batch array to be summarized by the LLM 
        batch_stories.append(f"{{index = {i}, headline = {headline}}}")
        i += 1
        # in independent arrays, store the headline, text, and media 
        post_headlines.append(headline)
        post_text.append(text)
        post_media.append(media)

    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(post_headlines)

    scaler = StandardScaler()
    embeddings = scaler.fit_transform(embeddings)

    # epsilon --> maximum distance between vectors in a neighborhood
    epsilon = 0.70
    # minimum number of vectors (posts) for a cluster to form 
    min_neighbors = 3

    # run DBSCAN clustering using cosine similarity
    db = DBSCAN(
        eps=epsilon, 
        min_samples=min_neighbors, 
        metric='cosine'
    ).fit(embeddings)

    # grab cluster assignments
    labels = db.labels_

    # find the number of clusters --> subtract 1 to account for "noise"
    num_clusters = len(set(labels))
    if -1 in labels:
        num_clusters -= 1

    # all noise stories are labeled -1. count the number of times this label appears
    num_noise_stories = list(labels).count(-1)

    # 5. Group headlines by their cluster ID
    grouped_stories = {}
    highlights = []
    news = []

    for headline, label, text, media in zip(post_headlines, labels, post_text, post_media):
        # Store noise points under the -1 key, and clusters under their ID
        if label not in grouped_stories:
            grouped_stories[label] = []
        grouped_stories[label].append((headline, text, media))

    for cluster_id, story_list in grouped_stories.items():
        # cluster representing noise (individual posts)
        if cluster_id == -1:
            # need to do regex matching to extract highlights
            pattern = r'highlight'
            for h, story_text, media in story_list:
                match = re.search(pattern, h, re.IGNORECASE)
                if match:
                    highlight_title = summarize_highlight(f"{h}, {story_text}")
                    highlights.append((highlight_title, media))
        else:
            prompt = '{'
            for h, story_text, media in story_list:
                prompt += f'Headline: {h}. '
                prompt += f'Story: {story_text}. '
            prompt += '}'
            summary = summarize_news_story(prompt)
            # regex match any text after headline and after the text sections. Regex match shoudl stop at any delimetter (, . or newline)
            pattern = r"Headline:\s*(.*?)[.,\s]*Story:\s*(.*)}"
            match = re.search(pattern, summary)
            if match:
                news.append({
                    "Headline" : match.group(1).strip(),
                    "Story" : match.group(2).strip()
                })
            else:
                raise Exception(f"Bad Output: {summary}")
            
    return {
        'news' : news, 'highlights' : highlights
    }

def user_authentication_email(email: str, password: str):
    response = supabase.auth.sign_in_with_password(
        {
            "email" : email,
            "password" : password
        }
    )

    return response

def write_summaries():
    # HARDCODE AUTH IN FOR NOW
    user = os.getenv('SUPABASE_ROOT_USER')
    passw = os.getenv('SUPABASE_ROOT_PW')

    # try to authenticate
    try:
        auth = user_authentication_email(user, passw)
    except Exception as e:
        print(e)

    # grab todays date
    todays_date = date.today().isoformat()

    # grab the data
    data = reddit_pipeline()
    news = data['news']
    highlights = data['highlights']

    # write out news stories
    for news_story in news:
        # build a mapping to the database field names
        database_fields_map = {
            'date' : todays_date,
            'headline' : news_story['Headline'],
            'story' : news_story['Story']
        }

        response = supabase.table("News").insert(database_fields_map).execute()
        print(response)
    
    # write out highlights
    for highlight_title, highlight_media in highlights:
        # build a mapping to the database field names
        database_fields_map = {
            'date' : todays_date,
            'title' : highlight_title,
            'media' : highlight_media
        }

        response = supabase.table("Highlights").insert(database_fields_map).execute()
        print(response)

write_summaries()

#TODO
'''
encapsulate and format the response information in a method 
format to be easily returned by an api request
'''