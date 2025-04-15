# # SearchService: performs web search using SerpAPI
# # SearchCounter: tracks and limits monthly searches
# # Integration with SearchCache from cache_module.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from cache_module import SearchCache

load_dotenv()

class SearchService:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.base_url = "https://serpapi.com/search"
        self.cache = SearchCache()

    def google_search(self, query, num_results=3):
        cached = self.cache.get(query, "google")
        if cached:
            print("Using cached results.")
            return cached

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            return [{"title": f"Error: {response.status_code}",
                     "link": "",
                     "snippet": "Error performing search."}]

        results = response.json().get("organic_results", [])
        formatted = [{
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", "")
        } for r in results[:num_results]]

        self.cache.set(query, "google", formatted)
        return formatted

    def google_news_search(self, query, num_results=3):
        cached = self.cache.get(query, "google_news")
        if cached:
            print("Using cached news results.")
            return cached

        params = {
            "engine": "google_news",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            return [{"title": f"Error: {response.status_code}",
                     "link": "",
                     "snippet": "Error performing news search.",
                     "date": ""}]

        results = response.json().get("news_results", [])
        formatted = [{
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", ""),
            "date": r.get("date", "")
        } for r in results[:num_results]]

        self.cache.set(query, "google_news", formatted)
        return formatted
