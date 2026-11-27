from config.llm_config import llm
from typing import Literal
from pydantic import BaseModel
from LangGraph.state  import  State
from langchain_core.messages import HumanMessage
import asyncio


class RouteDecision(BaseModel):
    agent: Literal['blog', 'linkedin', 'unclear']
    reason: str

router_llm = llm.with_structured_output(RouteDecision)


ROUTER_PROMPT = """You are a router. Read the user's request and pick one agent.
- blog: long-form article or blog post
- linkedin: LinkedIn post specifically, not a comment, reply, or message.
- unclear: use this when
    - no blog or LinkedIn post is named or clearly implied
    - the request asks for both
    - the request is for a comment reply, caption, video script, or another platform

Rule to mind if the request doesn’t name or clearly imply a blog or LinkedIn post, the answer is unclear, so the model stops guessing. 
Request: {request}"""


async def orchestrator_node(State):
    user_request= State['messages'][-1]
    prompt = ROUTER_PROMPT.format(request=user_request)
    decision= await router_llm.ainvoke(prompt)
    return {'route_decision': decision.agent,'route_reason':decision.reason}



