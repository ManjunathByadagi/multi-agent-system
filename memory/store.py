memory = []

def save(query, result):
    memory.append({
        "query": query,
        "result": result
    })

def get_memory():
    return memory