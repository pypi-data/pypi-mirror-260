
def add_context_lines_to_snippets(snippets, lines_before=100, lines_after=100):
    for i , snippet in enumerate(snippets):
        code = snippet.get('code')
        file_path = snippet.get('file_path')
        snippets[i]['code'] = add_context_to_snippet(file_path, code, lines_before=lines_before, lines_after=lines_after)

    return snippets


def add_context_to_snippet(file_path, snippet, lines_before=100, lines_after=100):
    """
    Extracts lines around a specific multi-line snippet from a file.

    :param file_path: Path to the file to be searched.
    :param snippet: Multi-line snippet of text to find in the file.
    :param lines_before: Number of lines to include before the snippet.
    :param lines_after: Number of lines to include after the snippet.
    :return: String containing the lines around the snippet.
    """
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # Join the file content and snippet into single strings to handle multi-line comparison
    content_str = ''.join(content)
    snippet_str = ''.join(snippet) if isinstance(snippet, list) else snippet
    
    snippet_start = content_str.find(snippet_str)
    
    if snippet_start == -1:
        return "Snippet not found in file."
    
    # Convert snippet start index from char index in joined string to line index in content list
    line_start_index = content_str[:snippet_start].count('\n') - lines_before
    snippet_end = snippet_start + len(snippet_str)
    line_end_index = content_str[:snippet_end].count('\n') + lines_after + 1
    
    # Adjust start and end indices to ensure they are within file bounds
    line_start_index = max(0, line_start_index)
    line_end_index = min(len(content), line_end_index)
    
    # Extract the lines around the snippet
    context_lines = content[line_start_index:line_end_index]
    res = ''.join(context_lines)
    return res
        