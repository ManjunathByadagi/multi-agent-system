import asyncio
from utils.search import search

# 🔍 Single research task (context-aware + filtered)
async def research_task(query, task):
    try:
        # 🔥 Focused query (IMPORTANT)
        full_query = f"{query} {task}"

        # 🔥 Domain filtering (healthcare-specific)
        if "healthcare" in query.lower():
            full_query += " healthcare AI real examples statistics"

        # 🔍 Call search
        results = search(full_query)

        # ❗ Handle empty results
        if not results:
            return f"{task}: No relevant data found."

        # 🔥 Limit results (prevents token overflow)
        limited_results = results[:2]

        # 🔥 Clean + trim each result
        cleaned = []
        for r in limited_results:
            text = r.strip().replace("\n", " ")
            cleaned.append(text[:300])  # limit each result

        combined = " ".join(cleaned)

        return f"{task}: {combined}"

    except Exception as e:
        return f"{task}: Error fetching data ({str(e)})"


# 🚀 Run all tasks in parallel
async def researcher(query, tasks):
    results = await asyncio.gather(
        *[research_task(query, t) for t in tasks]
    )

    return results