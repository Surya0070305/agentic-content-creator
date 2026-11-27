from langchain_core.messages import HumanMessage
import asyncio
from langgraph.types import interrupt, Command
from LangGraph.routing_graph import graph
from LangGraph.state import State

async def run_review_test():
    config = {"configurable": {"thread_id": "t3"}}   # fresh id
    request ="Write a blog post about electric vehicles in Indian cities"

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=request)]}, config
    )


    print(result)

    print('-------------------The initial draft------------------')
    print(result['output'])
    print('-'*40)
    print('Lenght of iteration--->', len(result['output']))
    print('-'*40)
    while result.get("__interrupt__"):
        print("PAUSED, counter:", result.get("revision_counter"))
        result = await graph.ainvoke(
            Command(resume={"decision": "Unsatisfied", "feedback": "Make it little formal and 3 bullet point per each topic"}),
            config,
        )
        print('-'*40)
        print(f'Lenght of iteration {result.get("revision_counter")}--->', len(result['output']))
        print(result['output'])
        print('-'*40)
        print('Eval Warnings--------->', result['eval_warning'])
        print('-'*40)
        print('Eval Score------------->', result['faithfulness_score'])

    print("satisfaction:", result["user_satisfaction"])
    print("Revision_Counter:", result["revision_counter"])
    print("final draft:", result["output"])
    print('Lenght of iteration--->', len(result['output']))

    print('Sources count---->', len(result['sources']))

if __name__ == "__main__":
    asyncio.run(run_review_test())
