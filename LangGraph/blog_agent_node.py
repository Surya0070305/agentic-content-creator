

from LangGraph.state import State
from main_server.Blog_Agent_Tool_Hub import blog_agent


async def blog_agent_node(State: State):
    current_agent='blog'
    user_request=State['messages'][-1].content.strip()


    if not user_request:
        return {
            'current_agent':current_agent,
            'error':'No input recieved from router/orchestrator'
        }

    topic=user_request

    feedback = ''
    previous_draft = ''

    if (State.get('revision_counter') or 0) > 0:
        feedback = State.get('user_feedback', '')
        previous_draft = State.get('output', '')

    output=await blog_agent(topic, feedback=feedback, previous_draft=previous_draft)

    if not output:
        return {
            'current_agent':current_agent,
            'error':'No output recieved from Blog Agent Tool'
        }

    if 'error' in output:
        return {
            'error':output['error'],
            'current_agent':current_agent,
        }


    return {
            'output': output['agent_output'],
            'current_agent': current_agent,
            'sources':output.get('sources',[]),
        }






