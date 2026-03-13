from tavily import TavilyClient
from config.config import TAVILY_API_KEY

def web_search(query: str) -> str:
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