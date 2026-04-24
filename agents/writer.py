from utils.llm import get_llm

llm = get_llm()

def writer(research_data):
    content = "\n".join(research_data[:3])

    content = content[:1500]

    prompt = f"""
You are an expert AI research analyst.

Write a HIGH-QUALITY, PROFESSIONAL report.

STRICT RULES:
- ONLY talk about the given topic
- Do NOT include unrelated industries
- Be specific and practical
- Add real-world examples
- Add numbers/statistics if possible
- Avoid generic sentences

STRUCTURE:

## Overview
(2–3 lines, very clear)

## Key Applications in Healthcare
- Use bullet points
- Add REAL examples (e.g., Google DeepMind, IBM Watson)

## Challenges (Real-world)
- Practical issues (data privacy, bias, cost)

## Future Trends
- What is actually happening next (not vague)

## 💡 Final Insight
- Strong, smart conclusion (1–2 lines max)

CONTENT:
{content}
"""

    response = llm.invoke(prompt)
    return response.content