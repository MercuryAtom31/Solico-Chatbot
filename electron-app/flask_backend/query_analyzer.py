# Logic to decide if the query requires real-time info
# Checks if the query is related to the printing industry
# Picks the appropriate search engine (Google vs Google News)

import re

class QueryAnalyzer:
    def __init__(self):
        self.current_info_keywords = [
            "latest", "current", "recent", "new", "today", "now",
            "update", "development", "news", "trend", "this year",
            "this month", "this week", "impact", "effect", "tariff",
            "regulation", "law", "policy", "price", "market"
        ]

        self.printing_keywords = [
            "print", "printer", "printing", "ink", "paper", "toner",
            "digital printing", "offset", "lithography", "flexography",
            "label", "packaging", "commercial print", "press", "printhead"
        ]

    def needs_current_info(self, query):
        q = query.lower()
        for keyword in self.current_info_keywords:
            if keyword in q:
                return True
        if re.search(r'\b20\d\d\b', q):
            return True
        if re.search(r'\b(impact|effect|change|influence)\b', q):
            return True
        return False

    def is_printing_related(self, query):
        q = query.lower()
        return any(k in q for k in self.printing_keywords)

    def determine_search_engine(self, query):
        if re.search(r'\b(news|recent|latest|update|development)\b', query.lower()):
            return "google_news"
        return "google"
