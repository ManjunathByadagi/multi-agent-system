import asyncio
from utils.search import search

# 🔍 Single research task (context-aware)
async def research_task(query, task):
    try:
        # Combine query + task (VERY IMPORTANT 🔥)
        full_query = f"{query} - {task}"
        
        results = search(full_query)

        # Join results safely
        combined = " ".join(results)

        return f"{task}: {combined}"

    except Exception as e:
        return f"{task}: Error fetching data - {str(e)}"


# ⚡ Run all tasks in parallel
async def researcher(query, tasks):
    results = await asyncio.gather(
        *[research_task(query, t) for t in tasks]
    )

    return results