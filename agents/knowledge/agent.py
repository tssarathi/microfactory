from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
import os

from .instruction import INSTRUCTION

KNOWLEDGE_MCP_URL = os.getenv("KNOWLEDGE_MCP_URL", "http://localhost:5002/mcp")

kb_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=KNOWLEDGE_MCP_URL),
    tool_filter=[
        "search_knowledge_base",
        "get_article",
        "list_articles",
    ],
)

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3.5:9b"),
    name="knowledge_agent",
    description="Technical knowledge specialist. Handles troubleshooting procedures, "
    "safety protocols, preventive maintenance schedules, Australian Standards "
    "references, and company SOPs for HVAC, electrical, plumbing, and "
    "refrigeration. Use this agent for HOW-TO questions, safety procedures, "
    "troubleshooting steps, and technical documentation lookups.",
    instruction=INSTRUCTION,
    tools=[kb_toolset],
    disallow_transfer_to_peers=True,
)
