import os

config_list = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": os.environ.get("GROQ_API_KEY"),
    "api_type": "groq"
}]

llm_config = {
    "config_list" : config_list,
    "temperature" : 0
}