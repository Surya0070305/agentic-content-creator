from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage
from LangGraph.state import State
from LangGraph.input_node import input_checks
from LangGraph.orchestrator_node import orchestrator_node
from LangGraph.blog_agent_node import blog_agent_node
from LangGraph.linkedin_agent_node import linkedin_agent_node
from LangGraph.output_node import output_checks
import asyncio
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


def route_after_input_checks(State):
    if State.get('error'):
        return 'end'
    return 'orchestrator'


def router_after_orchestrator(State):
    return State['route_decision']


def review_node(State):
    reply=interrupt({
        'draft':State.get('output'),
        'agent':State.get('current_agent')
    })


    return {
        'user_satisfaction':reply['decision'],
        'user_feedback':reply.get('feedback',''),
        'revision_counter':State.get('revision_counter',0)+1
    }


def route_after_review(State):

    if State.get('user_satisfaction')=='Satisfied':
        return 'done'
    if State.get('revision_counter')>4:
        return 'done'

    return State.get('current_agent')

builder= StateGraph(State)


#builder.add_node(START)
builder.add_node('input',input_checks)
builder.add_node('orchestrator',orchestrator_node)
builder.add_node('blog',blog_agent_node)
builder.add_node('linkedin',linkedin_agent_node)
builder.add_node('output',output_checks)
builder.add_node('review', review_node)




builder.add_conditional_edges(
    'input',
    route_after_input_checks,
    {'end':END, 'orchestrator':'orchestrator'}
)

builder.add_conditional_edges(
    'orchestrator',
    router_after_orchestrator,
    {'blog':'blog','linkedin':'linkedin','unclear':END}
)

builder.add_edge(START,'input')



builder.add_edge('blog','output')
builder.add_edge('linkedin','output')

builder.add_edge('output','review')

builder.add_conditional_edges(
    'review',
    route_after_review,
    {'done':END, 'blog':'blog', 'linkedin':'linkedin', 'unclear':END}
)

graph=builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "t2"}}







