import asyncio

from langchain_core.messages import HumanMessage

from LangGraph.output_node import output_checks

fake_state = {
    "messages": [HumanMessage(content="Write a blog post about electric vehicles in Indian cities")],
    "output": "Trichy has 5 million EV charging stations, and every car in India became electric in 2021.",
    "sources": ["Tamil Nadu aims to create 20,000 EV charging stations by 2031. EVs are about 10% of registrations in Tamil Nadu."],
}

result = asyncio.run(output_checks(fake_state))
print(result)