from fastmcp import FastMCP

from src.tools import search_knowledge

mcp = FastMCP("knowledge_base")

mcp.tool()(search_knowledge)

if __name__ == "__main__":
    mcp.run(transport="stdio")
