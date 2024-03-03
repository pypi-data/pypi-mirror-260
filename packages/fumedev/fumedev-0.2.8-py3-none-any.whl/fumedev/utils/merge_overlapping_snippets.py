def merge_overlapping_snippets(snippets,file_path):
    """
    Merges overlapping snippets into a single snippet, ensuring no redundant parts are recorded more than once.

    :param snippets: A list of tuples, each representing a snippet with (start_line, end_line, text).
    :return: A list of tuples representing merged and non-overlapping snippets.
    """
    tuple_snippets = []
    for snippet in snippets:
        tuple_snippets.append(snippet_to_tuple(file_path, snippet))

    snippets = tuple_snippets

    # Sort snippets by their start line
    snippets.sort(key=lambda x: x[0])

    merged_snippets = []
    for snippet in snippets:
        if not merged_snippets:
            merged_snippets.append(snippet)
            continue

        last_snippet = merged_snippets[-1]
        # Check if the current snippet overlaps with the last merged snippet
        if snippet[0] <= last_snippet[1]:
            # Calculate the new start, end, and merge texts while avoiding duplication
            new_start = min(last_snippet[0], snippet[0])
            new_end = max(last_snippet[1], snippet[1])

            # Determine the overlapping text portion and merge appropriately
            overlap_start_index = max(0, snippet[0] - last_snippet[0])
            non_overlap_text_last_snippet = last_snippet[2][:overlap_start_index]
            new_text = non_overlap_text_last_snippet + snippet[2]

            # Update the last merged snippet with the new merged details
            merged_snippets[-1] = (new_start, new_end, new_text)
        else:
            # No overlap, simply add the snippet to the list of merged snippets
            merged_snippets.append(snippet)

    return ['\n'.join(snippet[2]) for snippet in merged_snippets]


def snippet_to_tuple(file_path, snippet):
    """
    Converts a multi-line snippet from a file into a tuple (start_line, end_line, text)
    by searching for the exact snippet in the file.

    :param file_path: Path to the file containing the snippet.
    :param snippet: The multi-line snippet as a string.
    :return: A tuple (start_line, end_line, text) where text is a list of lines from the snippet.
             Returns None if the snippet is not found.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    file_content = ''.join(lines)
    snippet_content = snippet.strip()

    # Search for the snippet in the file content
    snippet_index = file_content.find(snippet_content)
    if snippet_index == -1:
        return None  # Snippet not found
    
    # Calculate start_line by counting the newlines before the snippet
    start_line = file_content[:snippet_index].count('\n') + 1

    # Calculate end_line by counting the newlines within the snippet
    end_line = start_line + snippet_content.count('\n')

    # Extract the text of the snippet as a list of lines
    snippet_lines = snippet_content.split('\n')

    return (start_line, end_line, snippet_lines)
