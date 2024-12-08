from app.ai.aigentext import generate
from app.ai.search_internet import ddg
from duckduckgo_search import AsyncDDGS



async def aisearch_internet(text, usr_id):
    ans = await ddg(text)
    query = await generate(f"Take a look at this question for you from the user:\n{text}\n-----\nWriting from the user's question, choose from this text {ans} the most appropriate answer, process and combine into a single answer, keep in mind that all links should remain exactly the same, and shorten the descriptions, do not try to say and comment that you you process and combine something, think that you found it yourself on the Internet and make some kind of summary, let the description be not particularly long, but also not very short, answer in the language in which the user's question was written", usr_id)
    if query is not None:
        return query
