import os
import faiss
import numpy as np

class VectorStore:
    def __init__(self, index_file, vector_dim, metric=faiss.METRIC_L2):
        """
        Initialize the VectorStore.

        :param index_file: Path to the FAISS index file.
        :param vector_dim: Dimension of the vectors.
        :param metric: Distance metric for the index (default: L2).
        """
        self.index_file = index_file
        self.vector_dim = vector_dim
        self.metric = metric

        if os.path.exists(index_file):
            self.index = self.load_index_from_disk(index_file)
        else:
            self.index = self.create_index(vector_dim, metric)

    def create_index(self, vector_dim, metric):
        """Create a FAISS index."""
        return faiss.IndexFlat(vector_dim, metric)

    def save_index_to_disk(self):
        """Save the FAISS index to disk."""
        faiss.write_index(self.index, self.index_file)

    def load_index_from_disk(self, file_path):
        """Load a FAISS index from disk."""
        return faiss.read_index(file_path)

    def add_vectors(self, vectors):
        """
        Add vectors to the FAISS index and return the index/indices at which they are added.

        :param vectors: A single vector or a 2D array of vectors.
        :return: The index (or indices) at which the vectors are added.
        """
        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors)

        # Reshape the vector to 2D if it is a single vector
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        vectors = vectors.astype('float32')

        # The index where the new vector(s) will be added is the current size of the index
        start_index = self.index.ntotal
        try:
            self.index.add(vectors)
        except AssertionError as e:
            return self.index.ntotal
        # If adding multiple vectors, return a range of indices
        end_index = self.index.ntotal
        if start_index + 1 == end_index:
            return start_index  # Single vector added
        else:
            return list(range(start_index, end_index))  # Multiple vectors added

    def search_vectors(self, query_vectors, k=5):
        """
        Search for the 'k' nearest neighbors of the query vectors.

        :param query_vectors: A single query vector or a 2D array of query vectors.
        :param k: Number of nearest neighbors to find.
        :return: distances and indices of the nearest neighbors.
        """
        if not isinstance(query_vectors, np.ndarray):
            query_vectors = np.array(query_vectors)

        # Reshape the vector to 2D if it is a single vector
        if query_vectors.ndim == 1:
            query_vectors = query_vectors.reshape(1, -1)

        query_vectors = query_vectors.astype('float32')
        distances, indices = self.index.search(query_vectors, k)
        return distances, indices
    
    def flush_index(self):
        """
        Flush the index, removing all vectors both from memory and disk.
        """
        # Remove the existing index file if it exists
        if os.path.exists(self.index_file):
            try:
                os.remove(self.index_file)
            except OSError as e:
                print(f"Error: {self.index_file} : {e.strerror}")
                return

        # Reset the in-memory index
        self.index = self.create_index(self.vector_dim, self.metric)

        # Save the new, empty index to disk
        self.save_index_to_disk()
