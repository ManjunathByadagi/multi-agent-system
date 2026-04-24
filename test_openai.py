from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  # ✅ correct
)

response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.choices[0].message.content)