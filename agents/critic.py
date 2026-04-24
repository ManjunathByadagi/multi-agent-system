from utils.llm import get_llm
import json
import re

llm = get_llm(temperature=0.2)  # 🔥 lower temp = more stable JSON

def extract_json(text):
    """
    Safely extract JSON from LLM response
    """
    # Remove code blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Try to find JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group()
    
    return None


def critic(draft):
    prompt = f"""
You are a strict AI evaluator.

Analyze the following answer and return ONLY VALID JSON.

Evaluation Criteria:
1. Relevance to query
2. Clarity and structure
3. Use of real-world examples
4. Depth (not generic)
5. Accuracy

Return EXACTLY in this format:

{{
  "score": 7.5,
  "issues": ["issue1", "issue2"],
  "improvements": ["improve1", "improve2"]
}}

STRICT RULES:
- Output ONLY JSON (no explanation)
- Score must be between 0 and 10
- Always include at least 1 issue
- Always include at least 1 improvement

ANSWER:
{draft}
"""

    try:
        response = llm.invoke(prompt)
        raw_text = response.content.strip()

        # 🔥 Extract clean JSON
        json_text = extract_json(raw_text)

        if not json_text:
            raise ValueError("No JSON found")

        result = json.loads(json_text)

        # 🔥 Safety checks
        if "score" not in result:
            result["score"] = 5

        if "issues" not in result:
            result["issues"] = ["Missing issues"]

        if "improvements" not in result:
            result["improvements"] = ["Improve clarity"]

        return result

    except Exception as e:
        return {
            "score": 5,
            "issues": ["Parsing failed"],
            "improvements": ["Rewrite with clearer structure"]
        }