import asyncio

from blog_agent_node import blog_agent_node
from langchain_core.messages import HumanMessage
from linkedin_agent_node import linkedin_agent_node
from orchestrator_node import orchestrator_node

test_cases = [
    ("Write a detailed blog post on how electric vehicles are changing city commuting.", "blog"),
    ("Create a LinkedIn post announcing that I completed my capstone project.", "linkedin"),
    ("Write an Instagram caption for my new cafe opening.", "unclear"),
]

async def run_manual_tests():
    for request, expected in test_cases:
        state = {"messages": [HumanMessage(content=request)]}

        # step 1: orchestrator fills route_decision and route_reason
        state.update(await orchestrator_node(state))
        actual = state["route_decision"]
        print(f"expected={expected} actual={actual}")

        # step 2: hand the same state to the matching agent node
        if actual == "blog":
            state.update(await blog_agent_node(state))
        elif actual == "linkedin":
            state.update(await linkedin_agent_node(state))
        else:
            state['output']='The request is unknown please try to fix the request and try again later'

        print("current_agent:", state.get("current_agent"))
        print("output:", (state.get("output") or "")[:150])
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_manual_tests())