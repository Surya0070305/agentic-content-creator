import requests

from dotenv import load_dotenv

import os




#CONFIG PARAMS


load_dotenv('secrets.env')

openai_key=os.environ["STABILITY_API_KEY"]

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
    headers={
        "authorization": openai_key,
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "Lighthouse on a cliff overlooking the ocean",
        "output_format": "png",
    },
)

if response.status_code == 200:
    with open("./lighthouse.png", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))