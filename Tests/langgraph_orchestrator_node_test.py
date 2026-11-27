from langchain_core.messages import HumanMessage
import asyncio
from LangGraph.orchestrator_node import orchestrator_node


async def run_test():

    for text in unclear_tests:
        state={'messages':[HumanMessage(text)]}
        print(text, "->", await (orchestrator_node(state)))

if __name__ == "__main__":
    unclear_tests = [
        'Reply to this comment on my post saying thanks.',
        'Write something about artificial intelligence.',
        'Help me share my project with people.'
    ]
    asyncio.run(run_test())