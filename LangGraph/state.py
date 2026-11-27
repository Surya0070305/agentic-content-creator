from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages


def merge_sources(old: list[str], new: list[str]) -> list[str]:
    combined = (old or []) + (new or [])
    return list(dict.fromkeys(combined))



class State(TypedDict):
    messages: Annotated[list, add_messages]
    route_decision:str
    route_reason:str
    route_score:dict[str, float]
    agent_params:dict[str, str]
    output:str
    current_agent:str
    user_satisfaction:Literal['Satisfied','Unsatisfied']|None
    user_feedback:str
    revision_counter:int
    error:str | None
    sources:Annotated[list[str], merge_sources]
    eval_warning:list[str]
    faithfulness_score: float | None