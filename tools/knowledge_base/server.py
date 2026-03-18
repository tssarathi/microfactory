from fastmcp import FastMCP

from src.tools import search_knowledge_base, get_article, list_articles

mcp = FastMCP("knowledge_base")

mcp.tool()(search_knowledge_base)
mcp.tool()(get_article)
mcp.tool()(list_articles)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=5002)
