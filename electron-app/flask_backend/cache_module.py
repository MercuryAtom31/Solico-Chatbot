
import os
import json
import hashlib
from datetime import datetime, timedelta

class SearchCache:
    def __init__(self, cache_dir="search_cache", cache_duration_days=7):
        self.cache_dir = cache_dir
        self.cache_duration = timedelta(days=cache_duration_days)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _generate_key(self, query, engine):
        key = f"{query}_{engine}"
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, query, engine):
        key = self._generate_key(query, engine)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")

        if not os.path.exists(cache_file):
            return None

        with open(cache_file, 'r') as f:
            cache_data = json.load(f)

        timestamp = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - timestamp > self.cache_duration:
            return None

        return cache_data['results']

    def set(self, query, engine, results):
        key = self._generate_key(query, engine)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")

        data = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "engine": engine,
            "results": results
        }

        with open(cache_file, 'w') as f:
            json.dump(data, f)
