from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

try:

    docs=[
        Document(
        page_content=item['text'],
        metadata={'title':item['title'],'source':item['link']}
    )

    for item in final_info
    ]
    print('The info has been converted into documents')

except Exception as e:
    print('Got the following error at document conversion---->',e)

def build_context(docs):
    parts = []
    for i, d in enumerate(docs, 1):
        parts.append(f"[{i}] {d.metadata['title']} ({d.metadata['source']})\n{d.page_content}")
    return "\n\n".join(parts)


formatted_docs=[build_context(docs)]


#print(formatted_docs[0][:500])



#Now we will be chunking the data which is in document format
def chunking(docs, chunk_size=800, chunk_overlap=120):
    chunks=[]
    for doc in formatted_docs:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        chunks=splitter.split_text(doc)

    return chunks

try:
    print('Building chunks')
    chunked_info=chunking(formatted_docs)
    print(f'Chunking done {len(chunked_info)} documents')
    #print(chunked_info[1])
except Exception as e:
    print('Got the following error at chunking---->',e)
