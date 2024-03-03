from concurrent.futures import ThreadPoolExecutor
import concurrent
import json
import os

from dotenv import load_dotenv
from pathlib import Path

from fumedev.env import absolute_path
from fumedev import env
load_dotenv()

from fumedev.index.FolderGraph import FolderGraph
from fumedev.index.VectorStore import VectorStore
from fumedev.index.utils.get_emmbedding import get_embedding
from fumedev.index.utils.line_chunker import line_chunker
from fumedev.utils.filter_snippets_header import filter_snippets_header

"""
Documentation class processes and handles the documentation of code snippets within the given root codebase directory.
It supports operations such as document processing and indexing, snippet vectorization, and code searching with vector similarity.
"""
class Documentation():
    def __init__(self, root_folder=absolute_path('codebase')):
        self.snippet_docs = []
        self.root_folder = root_folder

        self.db = None
        self.index = {}
        self.vector_index = VectorStore(absolute_path('snippets_index.idx'), 3072)
        self.embedded_snippets = []

    def document(self):
        """
        Processes all files in the root directory to extract code snippets, and vectorizes and indexes these snippets for search.
        It flushes existing snippet indexes and rebuilds them from scratch based on the current state of the codebase.
        """
        
        if os.path.exists(absolute_path('snippets_code.json')):
            os.remove(absolute_path('./snippets_code.json'))

        if os.path.exists(absolute_path('snippets_index.idx')):     
            self.vector_index.flush_index()

        fg = FolderGraph(root_folder=self.root_folder)
        files = fg.get_leaf_files()

        file_dict_list = []
        for file in files:
            file_dict_list.append(self.process_file(file))
                
                    
        self.vectorize_snippets(file_dict_list) 

    def process_file(self, file):
        try:
            snippets = line_chunker(file, 20)
        except:
            return
        
        for i,snippet in enumerate(snippets):
            snippets[i] = f'File Path: {file}\n\n{snippet}'

        file = {
            'file_path': file,
            'snippets': snippets
        }
        return file

    """
    Takes the extracted snippets from a file, vectorizes them, and saves them for indexing.

    Args:
        file (dict): A dictionary containing the file path and the snippets to be saved and indexed.
    """
    def save_snippet_code(self, file):
        file_path = file.get('file_path')
        snippets = file.get('snippets')

        for snippet in snippets:
            # Compute the document embedding
            doc_vec = get_embedding(snippet)

            embedded_snippet = {
                'code': snippet,
                'file_path': file_path,
                'embedding': doc_vec
            }
            self.embedded_snippets.append(embedded_snippet)
        
    """
    Searches the indexed code snippets for instances most similar to the query.

    Args:
        query (str): The query string to search for.
        k (int, optional): The number of results to return. Defaults to 5.
        extension (str, optional): Filter results by file extension. Defaults to None.
        iteration (int, optional): Used internally for recursive refining of search results. Defaults to 1.
        file_path (str, optional): Filter results by file path. Defaults to ''.

    Returns:
        list: A list of dictionaries each containing a matching code snippet and its file path.
    """
    def search_code(self, query, k=5, extension=None, iteration=1, file_path=''):

        if iteration > 500:
            return False

        # Calculate query embeddings
        q = get_embedding(query)
        distances, indices = self.vector_index.search_vectors(query_vectors=q, k=k*iteration)
        distances = distances[0]
        indices = indices[0]

        with open(absolute_path('snippets_code.json'), 'r') as file:
            snippets_data = json.load(file)

        # Initialize list to hold filtered snippets with their distances
        filtered_snippets = []
        
        for i, index in enumerate(indices):
            index_str = str(index)  # Convert index to string to match keys in snippets_data
            if index_str in snippets_data:
                snippet = snippets_data[index_str]
                snippet = filter_snippets_header([snippet])[0]
                snippet_path = snippet['file_path']
                snippet_already_in_results = False
                for snippet_in_result in env.SNIPPETS:
                    if snippet_in_result['code'] == snippet['code'] and snippet_in_result['file_path'] == snippet['file_path']:
                        snippet_already_in_results = True
                        break
                if snippet_already_in_results or snippet['code'].isspace():
                    continue
                if file_path and file_path in snippet_path:
                    filtered_snippets.append((distances[i], snippet))
                elif extension and snippet_path.endswith('.' + extension):
                    filtered_snippets.append((distances[i], snippet))
                elif not file_path and not extension:
                    filtered_snippets.append((distances[i], snippet))

        # Sort snippets by distance
        filtered_snippets.sort(key=lambda x: x[0])

        # Prepare return list, eliminating potential duplicates by using a set
        results = []
        for _, snippet in filtered_snippets:
            results.append({'file_path': snippet['file_path'], 'code': snippet['code']})

            if len(results) == k:
                break

        if len(results) < k:
            new_results = self.search_code(query=query, k=k, extension=extension, iteration=iteration+1, file_path=file_path)

            if new_results:
                results = new_results
        
        return results

    """
    A wrapper for search_code to format results specific to the application's needs, filtering by snippet relevance.

    Args:
        query (str): The search query string.
        k (int, optional): The number of results to return. Defaults to 5.
        extension (str, optional): Filter results by file extension. Defaults to None.

    Returns:
        list: A list of formatted results each containing a code snippet and its file path.
    """
    def get_relevant_codes(self, query, k=5, extension=None):
        docs = self.search_code(query=query, k=k, extension=extension)
        res = []
        for doc in docs:
            snippet = doc.get('code')
            file_path = doc.get('file_path')
            res.append({'snippet': snippet, 'file_path': file_path})

        return res

    def vectorize_snippets(self, files):
        with ThreadPoolExecutor(max_workers=60) as executor:  # Adjust max_workers as needed
            future_to_snippet = {executor.submit(self.save_snippet_code, file): file for file in files}
            for future in concurrent.futures.as_completed(future_to_snippet):
                file = future_to_snippet[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print(f'Sorry, bumbed in to a mistake indexing file: {file.get("file_path")} \n {exc}')
                


        for snippet in self.embedded_snippets:
            idx = self.vector_index.add_vectors(snippet.get('embedding'))

            self.index[idx] = {
            'code': snippet.get('code'),
            'file_path': snippet.get('file_path')  
            }  # No need to convert to list
             
        json_file_path = absolute_path('snippets_code.json')
        with open(json_file_path, 'w') as file:
            json.dump(self.index, file)

        self.vector_index.save_index_to_disk()        
        json_file_path = absolute_path('snippets_code.json')
        with open(json_file_path, 'w') as file:
            json.dump(self.index, file)

