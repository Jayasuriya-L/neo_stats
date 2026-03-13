import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ddgs import DDGS
from config.config import MAX_SEARCH_RESULTS


def web_search(query, max_results=None):
    """
    Perform a real-time web search using DuckDuckGo (no API key required).
    Returns results formatted as a context string for the LLM.
    """
    if max_results is None:
        max_results = MAX_SEARCH_RESULTS

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No web search results found for this query."

        context_parts = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            body = result.get("body", "No content")
            href = result.get("href", "")
            context_parts.append(f"[Result {i}] {title}\n{body}\nSource: {href}")

        print(f"Web search context:\n{context_parts}")  # Debugging output
        return "\n\n".join(context_parts)

    except Exception as e:
        return f"Web search failed: {str(e)}"
