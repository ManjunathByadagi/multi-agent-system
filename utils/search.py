from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search(query):
    response = client.search(query=query, max_results=3)
    return [r["content"] for r in response["results"]]