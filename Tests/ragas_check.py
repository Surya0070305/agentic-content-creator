import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ragas import SingleTurnSample
from ragas.metrics import Faithfulness

env_path = Path(__file__).parent.parent / "secrets.env"
load_dotenv(env_path)
openai_key=os.environ["OPEN_AI_KEY"]
os.environ["OPENAI_API_KEY"] = os.environ["OPEN_AI_KEY"]



llm = ChatOpenAI(
    api_key=openai_key,
    model="gpt-4o-mini",
    # stream_usage=True,
    temperature=0,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    # base_url="...",
    # organization="...",
    # other params...
)

context = [
    "Electric vehicles now account for over 33% of new three-wheeler sales in India, "
    "making it the first vehicle segment to cross that mark. Mahindra has sold more than "
    "400,000 electric last-mile vehicles, including over 100,000 in a single year. "
    "These sales have helped avoid more than 180,000 metric tons of carbon dioxide emissions. "
    "Mahindra aims to have one million electric vehicles on Indian roads by 2031."
]

user_input = "Write a short blog about electric vehicles in India."

responses = {
    # expect close to 1.0: every claim is in the context
    "faithful": "Electric three-wheelers now make up over 33% of new sales in India. "
                "Mahindra has sold more than 400,000 electric last-mile vehicles.",

    # expect around 0.5: two claims supported, two invented
    "partial":  "Electric three-wheelers make up over 33% of new sales in India. "
                "Mahindra aims for one million EVs by 2031. "
                "India has 50,000 public charging stations. "
                "The government gives every EV buyer a 2 lakh rupee subsidy.",

    # expect close to 0.0: nothing here is in the context
    "invented": "Tesla opened its first Indian factory in Pune last year. "
                "EV prices in India have fallen by 60% since 2020.",
}


faithfulness_llm= Faithfulness(llm=llm)


async def ragas_check():
    for name, response in responses.items():
        sample=SingleTurnSample(
            user_input=user_input,
            response=response,
            retrieved_contexts=context
        )

        score= await faithfulness_llm.single_turn_ascore(sample)

        print(f'{name}: {score}')



if __name__ == "__main__":
    asyncio.run(ragas_check())



