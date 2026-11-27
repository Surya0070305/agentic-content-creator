from langchain.mcp import MCPAdapter
import asyncio
import json
from config.extract_helper import source_text


client = MCPAdapter({
    "linkedin":  {"url": "http://localhost:8001/mcp", "transport": "streamable-http"}
})


async def linkedin_agent(topic, previous_draft='', feedback=''):
    try:
        tools = await client.list_tools()
    except Exception as e:
        return {'error': str(e)}
    print('previous draft:', previous_draft[:250])
    print('feedback:', feedback[:250])
    linkedin_tools = {t.name:t for t in tools}
    tool=linkedin_tools['Post_Generation']
    result= await tool.ainvoke(
    {
        'topic':topic,
        'previous_draft':previous_draft,
        'feedback':feedback,
    }
    )

    final_output = result[0]['text']
    data = json.loads(final_output)

    tool_output = data['draft']

    sources = source_text(data)



    return {'agent_output':tool_output, 'sources':sources}


