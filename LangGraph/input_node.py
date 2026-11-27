from guardrails.utils import on_fail
from presidio_anonymizer.entities.engine import pii_entity

from LangGraph.state import State
from langchain_core.messages import HumanMessage
from guardrails import Guard
import os
from pathlib import Path
from dotenv import load_dotenv
from guardrails.errors import ValidationError
from guardrails_ai.toxic_language import ToxicLanguage
from guardrails_ai.detect_pii import DetectPII
from guardrails_ai.nsfw_text import NSFWText
from guardrails_ai.prompt_injection_detector import PromptInjectionDetector





env_path = Path(__file__).parent.parent / "secrets.env"
load_dotenv(env_path)
openai_key=os.environ["OPEN_AI_KEY"]
os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]


guard = Guard().use(

    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="exception"),
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="exception"),


)



prompt_guard = Guard().use(
PromptInjectionDetector(llm_callable='gpt-4o-mini',api_key=openai_key,on_fail="exception")
)

nsfw_guard = Guard().use(
NSFWText(threshold=0.95, validation_method="sentence", on_fail="exception")
)



def input_checks(State):
    user_message= State.get("messages")[-1].content
    #print(user_message)
    #print('Type--->',type(user_message))

    user_input = user_message.strip().split()

    if not user_input:
        return {
            'error':'Please provide the input'
        }


    if len(user_input)<5:
        return {
            'error':'the input is under lenght, the user needs to give more defined way '
        }


    if len(user_input)>50:
        return {
            'error':'The user input is huge, can the user be more specific rather than more descriptive'
        }


    try:
        guard.validate(user_message)

    except ValidationError as e:
        return {'error':f"Request blocked by safety checks: {e}"}

    except Exception as e:
        return {"error": f"Safety check unavailable, please try again later: {e}"}


    try:
        prompt_guard.validate(user_message)

    except ValidationError as e:
        return {'error':f"Request blocked by safety checks: {e}"}

    except Exception as e:
        return {"error": f"Safety check unavailable, please try again later: {e}"}


    try:
        nsfw_guard.validate(user_message)

    except ValidationError as e:
        return {'error':f"Request blocked by safety checks: {e}"}

    except Exception as e:
        return {"error": f"Safety check unavailable, please try again later: {e}"}




    return {
        'error':None,
        'revision_counter':0,
        'user_feedback':'',
        'user_satisfaction':None
    }






