from langchain_core.messages import HumanMessage
from LangGraph.linkedin_agent_node import linkedin_agent_node
import asyncio

async def run_test():

    for text in unclear_tests:
        state={'messages':[HumanMessage(text)]}
        print(text, "->", await (linkedin_agent_node(state)))

if __name__ == "__main__":
    unclear_tests = [
        'Create a LinkedIn post announcing that I completed my agentic AI capstone project.',
        '- Write a short professional post about three lessons I learned from building AI agents.'
    ]
    asyncio.run(run_test())