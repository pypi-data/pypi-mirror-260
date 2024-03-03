
def filter_snippets_header(snippets):
    for i,snippet in enumerate(snippets):
        code = snippet.get('code')
        code = code.split('\n')[2:]
        code = '\n'.join(code)
        snippets[i]['code'] = code
    
    return snippets
        