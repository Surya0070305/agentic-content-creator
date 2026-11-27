import json

from langchain.mcp import MCPAdapter

from config.extract_helper import source_text

client = MCPAdapter({
    "blog":  {"url": "http://localhost:8000/mcp", "transport": "streamable-http"}
})

async def blog_agent(topic, feedback='', previous_draft=''):
    try:
        tools = await client.list_tools()
    except Exception as e:
        return {'error': str(e)}


    print('previous draft:', previous_draft[:250])
    print('feedback:', feedback[:250])

    blog_tools = {t.name:t for t in tools}
    tool=blog_tools['blog_generation']
    result= await tool.ainvoke(
    {
        'topic':topic,
        'previous_draft':previous_draft,
        'feedback':feedback,
    }
    )

    final_output=result[0]['text']
    data=json.loads(final_output)

    tool_output=data['draft']

    sources=source_text(data)

    return {'agent_output':tool_output, 'sources':sources}


