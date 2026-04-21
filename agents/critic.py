from utils.llm import get_llm
import json

llm = get_llm()

def critic(draft):
    prompt = f"""
    Evaluate this content.

    Return JSON:
    {{
      "score": float,
      "issues": [],
      "improvements": []
    }}

    Content:
    {draft}
    """

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return {"score": 5, "issues": ["Parsing failed"], "improvements": []}