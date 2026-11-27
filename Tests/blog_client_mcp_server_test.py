
import asyncio
import json

from langchain.mcp import MCPAdapter

client = MCPAdapter({
    "blog":  {"url": "http://localhost:8000/mcp", "transport": "streamable-http"}
})

async def test_blog_tool():
    tools = await client.list_tools()
    tool = {t.name: t for t in tools}["blog_generation"]

    # test 1: first pass, topic only
    first = await tool.ainvoke({"topic": "electric scooters in Indian cities"})
    draft = first[0]["text"]
    data=json.loads(draft)
    tool_output=data['draft']

    context=[]
    for source in data['sources']:
        articles=json.loads(source)
        for article in articles:
            if article['text']:
                context.append(article['text'])
                #print('\n---------------SOURCE-----------\n',article)
    print(len(context))


    print(context)

    #print("FIRST PASS:\n", tool_output, "\n")

    #print("SOURCES:\n", sources, "\n")

    #print(sources)

    # test 2: revision, topic + previous draft + feedback
    revised = await tool.ainvoke({
        "topic": "electric scooters in Indian cities",
        "previous_draft": draft,
        "feedback": "Make it much shorter, around 150 words, and drop the sources section.",
    })
    print("REVISED:\n", revised[0]["text"])
    print("revised length:", len(revised[0]["text"]), "vs first:", len(draft))



if __name__ == "__main__":
    asyncio.run(test_blog_tool())
