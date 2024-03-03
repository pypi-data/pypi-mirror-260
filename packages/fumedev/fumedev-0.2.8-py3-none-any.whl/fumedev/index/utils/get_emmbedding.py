import hashlib
import os
import json
from openai import OpenAI

from fumedev import env

cache_dir = env.absolute_path("./cache/embedding_cache")

class LocalCache:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _generate_hash_key(self, text):
        # Generate a SHA-256 hash of the text
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def _get_cache_path(self, text):
        # Generate hash key for the filename
        key = self._generate_hash_key(text)
        return os.path.join(self.cache_dir, f"{key}.json")


    def get(self, text):
        path = self._get_cache_path(text)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None

    def set(self, text, value):
        path = self._get_cache_path(text)
        with open(path, 'w') as f:
            json.dump(value, f)

cache = LocalCache(cache_dir)




def get_embedding(text):
        

        if text == '':
            return []

        # Check cache first
        cached_result = cache.get(text)
        if cached_result is not None:
            return cached_result
        
         
        # Fetch from API and cache
        client = OpenAI(api_key=env.OPENAI_API_KEY,base_url=env.BASE_URL)
        response = client.embeddings.create(input=[text], model="text-embedding-3-large",)
        embedding = response.data[0].embedding
        cache.set(text, embedding)
        return embedding
