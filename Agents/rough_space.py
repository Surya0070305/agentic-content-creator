from importlib.metadata import metadata

import trafilatura
from dotenv import load_dotenv
from serpapi import GoogleSearch
import os
import tiktoken




MAX_TOKENS=6000
enc = tiktoken.get_encoding('cl100k_base')
load_dotenv('secrets.env')

try:
    serp_api_key=os.environ["SERP_API_KEY"]
    print('SERP_API_KEY is initialized!!!')

except KeyError:
    print('SERP_API_KEY is not set!!!')


topic='gaming console'#This should be given by orchestrator

params={
  "engine": "google",
  "q": topic,
  "hl": "en",
    "tbm": "nws",
  "api_key": serp_api_key
}

results=GoogleSearch(params).get_dict()
#print(results.keys())
#print(results['news_results'][0]['link'])



#print(results)

final_info=[]
if results:
    print('Found results entered into the loop')
    for i in range(3):
        if i==3:
            break
        link=results['news_results'][i]['link']#need to fix this part
        #print('link:', type(link), link)
        downloaded_info=trafilatura.fetch_url(link)
        #print("downloaded:", type(downloaded_info), len(downloaded_info) if downloaded_info else 0)

        text = None
        meta_info = None

        if downloaded_info:
            text=trafilatura.extract(downloaded_info,include_comments=False, include_tables=False)
            token = enc.encode(text)
            decoded_text_with_capping = enc.decode(token[:MAX_TOKENS])
            #print("text length:", len(text) if text else 0)
            meta_info=trafilatura.extract_metadata(downloaded_info)
            #print("meta:", meta_info)
            #print("title:", getattr(meta_info, "title", None))
        else:
            print("No results")


        #print(meta_info.title if meta_info else None)
        #print(text[:1000] if text else None)
        title=meta_info.title if meta_info else None
        formatted_info={
            'title': title,
            'link': link,
            'text': decoded_text_with_capping,
        }

        final_info.append(formatted_info)


else:
    print("No results")



