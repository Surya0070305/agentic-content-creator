



import os
from pathlib import Path

from dotenv import load_dotenv
from guardrails import Guard
from guardrails.errors import ValidationError
from guardrails_ai.detect_pii import DetectPII
from guardrails_ai.nsfw_text import NSFWText
from guardrails_ai.toxic_language import ToxicLanguage
from langchain_openai import ChatOpenAI
from ragas import SingleTurnSample
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import Faithfulness

env_path = Path(__file__).parent.parent / "secrets.env"
load_dotenv(env_path)
openai_key=os.environ["OPEN_AI_KEY"]
os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]



ragas_llm = ChatOpenAI(
    api_key=openai_key,
    model="gpt-4o-mini",
    temperature=0,
)

faithfulness_llm= Faithfulness(llm=LangchainLLMWrapper(ragas_llm))

guard = Guard().use(

    ToxicLanguage(threshold=0.5, validation_method="full", on_fail="exception"),
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="exception"),

)



nsfw_guard = Guard().use(
NSFWText(threshold=0.9, validation_method="full", on_fail="exception")
)

async def output_checks(State):
    warning = []
    user_message= State.get("messages")[0].content
    draft=State.get("output")
    sources=State.get("sources") or []


    try:
        guard.validate(draft)

    except ValidationError as e:
        warning.append(f"Output check flagged: {e}")

    except Exception as e:
        warning.append(f"Safety check unavailable: {e}")


    try:
        nsfw_guard.validate(draft)

    except ValidationError as e:
        warning.append(f"Output check flagged: {e}")

    except Exception as e:
        warning.append(f"Safety check unavailable: {e}")

    score=None
    if sources:
        sample_check=SingleTurnSample(
            user_input=user_message,
            response=draft,
            retrieved_contexts=sources,
        )



        try:
            score = await faithfulness_llm.single_turn_ascore(sample_check)
            if score< 0.7:
                warning.append(f"Low faithfulness: {score:.2f}")

        except Exception as e:
            warning.append(f"Faithfulness check unavailable------>{e}")





    return {
       'eval_warning': warning,
       'faithfulness_score':score
    }

