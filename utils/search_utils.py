# utils/search_utils.py
# Handles live web search using Tavily
# Called when user enables web search
# and no document context is available

from tavily import TavilyClient
from config.config import TAVILY_API_KEY


def web_search(query: str) -> str:
    """
    Searches the web and returns summarized results.
    
    WHY TAVILY?
    - Free (1000 searches/month)
    - Returns clean text, not raw HTML
    - AI-optimized search results
    
    HOW TO EXTEND:
    - Filter by domain?  add include_domains=["wikipedia.org"]
    - News only?         add topic="news"
    - More results?      increase max_results
    - Show URLs?         add r['url'] to formatted output
    """
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)

        response = client.search(
            query=query,
            max_results=3,
            search_depth="basic"
        )

        results = response.get("results", [])

        if not results:
            return "No web results found."

        # Format results into readable text for the LLM
        formatted = []
        for r in results:
            formatted.append(
                f"Source: {r.get('title', 'Unknown')}\n"
                f"Summary: {r.get('content', '')}"
            )

        return "\n\n".join(formatted)

    except Exception as e:
        print(f"[WEB SEARCH ERROR] {e}")
        return f"Web search failed: {str(e)}"