from fumedev.index.Documentation import Documentation
from fumedev.lllm_utils.rerank_snippets import rerank_snippets

def search_snippet(query, extension='', file_path='', k=2, rerank=True):
    doc = Documentation()
    snip_lst = doc.search_code(query=query, extension=extension, file_path=file_path, k=k+20)

    if rerank and snip_lst:
        snip_lst = rerank_snippets(query=query, snippets=snip_lst)[:k]

    return snip_lst, [snip.get('file_path') for snip in snip_lst]



