import asyncio

from langchain_core.messages import HumanMessage

from LangGraph.blog_agent_node import blog_agent_node


async def run_test():

    for text in unclear_tests:
        state={'messages':[HumanMessage(text)]}
        print(text, "->", await (blog_agent_node(state)))

if __name__ == "__main__":
    unclear_tests = [
        'Write a detailed blog post on how electric vehicles are changing city commuting',
        'Write an article about the history of the Black Myth Wukong game'
    ]
    asyncio.run(run_test())