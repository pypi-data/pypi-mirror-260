import cohere
import fumedev.env as env

co = cohere.Client(env.COHERE_API_KEY)


def rerank_snippets(query, snippets):

    docs = [snippet.get('code') for snippet in snippets]

    results = co.rerank(query=query, documents=docs, top_n=3, model='rerank-english-v2.0') # Change top_n to change the number of results returned. If top_n is not passed, all results will be returned.
    new_snippets = []
    for idx, r in enumerate(results):
        if r.relevance_score < 0.2:
            continue
        else:
            new_snippets.append(snippets[r.index])

    return new_snippets