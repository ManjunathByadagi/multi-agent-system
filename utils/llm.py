from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

#  ENV VARIABLES
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

#  FIXED DEFAULT MODEL (WORKING)
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")

#  If key missing → stop immediately
if not API_KEY:
    raise ValueError(" OPENAI_API_KEY not set. Add it in .env file")

#  DEBUG (VERY IMPORTANT)
print(" LLM DEBUG INFO")
print("MODEL:", MODEL)
print("BASE URL:", BASE_URL)
print("API KEY (partial):", API_KEY[:10] + "...")

#  MAIN LLM FUNCTION
def get_llm(temperature=0.7):

    return ChatOpenAI(
        model=MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,

        #  Stability settings
        temperature=temperature,
        timeout=60,
        max_retries=2,

         max_tokens=800,
         
        #  OpenRouter headers
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Multi-Agent Research System"
        }
    )