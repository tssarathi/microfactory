from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
import os

from .instruction import INSTRUCTION

DATABASE_MCP_URL = os.getenv("DATABASE_MCP_URL", "http://localhost:5001/mcp")

db_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=DATABASE_MCP_URL),
    tool_filter=[
        "get_available_technicians",
        "get_technician_details",
        "get_technician_schedule",
        "get_technician_certifications",
        "check_certification_compliance",
        "search_available_slots",
    ],
)

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3.5:9b"),
    name="scheduling_agent",
    description="Scheduling and dispatch advisory. Manages technician availability, "
    "schedule lookups, certification compliance checks, and dispatch "
    "recommendations for HVAC, electrical, plumbing, and refrigeration "
    "field service operations.",
    instruction=INSTRUCTION,
    tools=[db_toolset],
    disallow_transfer_to_peers=True,
)
