# config.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pathlib import Path

env_path = Path(__file__).parent.parent / "secrets.env"
load_dotenv(env_path) # reads OPENAI_API_KEY from your .env file
#print('The current directory---->',load_dotenv('secrets.env'))
openai_key=os.environ["OPEN_AI_KEY"]

try:
    llm = ChatOpenAI(
    api_key=openai_key,
    model="gpt-4o-mini",
    temperature=0
    )
    print('LLm  is initialized')

except Exception as e:
    print(e)