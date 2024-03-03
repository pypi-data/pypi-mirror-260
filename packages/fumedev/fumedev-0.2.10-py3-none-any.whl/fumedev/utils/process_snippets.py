from fumedev.utils.add_context_lines_to_snippets import add_context_lines_to_snippets
from fumedev.utils.merge_overlapping_snippets import merge_overlapping_snippets


def process_snippets(snippets, lines_before=100, lines_after=100):
    snippets = add_context_lines_to_snippets(snippets, lines_before=lines_before, lines_after=lines_after)
    files = {}
    res = []
    for snippet in snippets:
        file_path = snippet.get('file_path')
        if file_path not in files.keys():
            files[file_path] = []
        files[file_path].append(snippet.get('code'))

    for file_path , snippet_list in files.items():
        files[file_path] = merge_overlapping_snippets(snippets=snippet_list, file_path=file_path)

    
    for file_path , snippet_list in files.items():
        for snippet in snippet_list:
            res.append({
                'file_path': file_path,
                'code': snippet
            })


    return res

        
