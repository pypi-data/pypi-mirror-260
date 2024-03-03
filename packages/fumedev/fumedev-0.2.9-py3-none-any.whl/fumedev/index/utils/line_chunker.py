def line_chunker(file_path, max_lines_per_chunk):
    """
    Splits the content of a file into chunks, each containing up to max_lines_per_chunk lines.
    
    :param file_path: Path to the input file.
    :param max_lines_per_chunk: Maximum number of lines per chunk.
    :return: A list of strings, each string is a chunk of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunks = []
    for i in range(0, len(lines), max_lines_per_chunk):
        chunk = ''.join(lines[i:i+max_lines_per_chunk])
        chunks.append(chunk)

    return chunks
