from langchain.mcp import MCPAdapter
import asyncio
import json

client = MCPAdapter({
    "linkedin":  {"url": "http://localhost:8001/mcp", "transport": "streamable-http"}
})

async def test_blog_tool():
    tools = await client.list_tools()
    tool = {t.name: t for t in tools}["Post_Generation"]

    # test 1: first pass, topic only
    first = await tool.ainvoke({"topic": "LTC Hyderabad"})
    # print(first)

    draft = first[0]["text"]
    # print(draft)

    data = json.loads(draft)
    tool_output = data['draft']

    # print(tool_output)

    context = []
    for source in data['sources']:
        articles = json.loads(source)
        for article in articles:
            if article['text']:
                context.append(article['text'])
                # print('\n---------------SOURCE-----------\n',article)
    print(len(context))

    print(context)
    '''
    # test 2: revision, topic + previous draft + feedback
    revised = await tool.ainvoke({
        "topic": "LTC Hyderabad",
        "previous_draft": draft,
        "feedback": "Make it more formal , structured , with more hashtags",
    })
    print("REVISED:\n", revised[0]["text"])
    print("revised length:", len(revised[0]["text"]), "vs first:", len(draft))
    '''


if __name__ == "__main__":
    asyncio.run(test_blog_tool())

'''
if __name__ == "__main__":
    topic = input("Topic: ")
    print(asyncio.run(linkedin_agent(topic)))
'''