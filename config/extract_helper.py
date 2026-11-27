import json

def source_text(data):
    context=[]
    for source in data['sources']:
        articles=json.loads(source)
        for article in articles:
            if article.get('text'):
                context.append(article.get('text'))

    return context