from utils.llm import get_llm

llm = get_llm()

def writer(research_data):
    content = "\n".join(research_data)

    prompt = f"""
    Write a clean, structured answer.

    Rules:
    - Use headings (##)
    - Use bullet points
    - Keep paragraphs short
    - Make it easy to read
    - Avoid long blocks of text

    Content:
    {content}
    """

    response = llm.invoke(prompt)
    return response.content