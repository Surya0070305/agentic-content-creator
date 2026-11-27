from langfuse.api import feedback

from LangGraph.state import State
from main_server.LinkedIN_Agent_Tool_Hub import linkedin_agent
import asyncio
from langchain_core.messages import HumanMessage

async def linkedin_agent_node(State: State):
    current_agent='linkedin'
    user_request=State['messages'][-1].content.strip()


    if not user_request:
        return {
            'current_agent':current_agent,
            'error':'No input recieved from router/orchestrator'
        }

    topic=user_request

    feedback=''
    previous_draft=''

    if (State.get('revision_counter') or 0) > 0:
        feedback=State.get('user_feedback','')
        previous_draft=State.get('output','')

    output=await linkedin_agent(topic, feedback=feedback, previous_draft=previous_draft)

    if not output:
        return {
            'current_agent':current_agent,
            'error':'No output recieved from LinkedIN Agent Tool'
        }

    if 'error' in output:
        return {
            'error':output['error'],
            'current_agent':current_agent,
        }

    return {
        'output': output['agent_output'],
        'current_agent': current_agent,
        'sources': output.get('sources', []),
    }



