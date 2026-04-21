from utils.llm import get_llm
import json
import re

llm = get_llm()

def planner(query):
    prompt = f"""
    Break the query into subtopics.

    Return ONLY a JSON list.
    Example:
    ["Overview", "Applications", "Challenges"]

    Query: {query}
    """

    response = llm.invoke(prompt)
    text = response.content.strip()

    # 🔥 Remove markdown (```json or ```python)
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "")

    try:
        tasks = json.loads(text)
    except:
        tasks = ["Overview", "Applications", "Challenges"]

    return tasks