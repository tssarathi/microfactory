from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from pathlib import Path


from .instruction import INSTRUCTION

TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"

db_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", str(TOOLS_DIR / "database/server.py")],
        ),
    ),
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
    model=LiteLlm(model="openai/qwen3:8b"),
    name="scheduling_agent",
    description="Scheduling and dispatch specialist. Manages technician availability, "
    "schedule lookups, certification compliance checks, and dispatch "
    "recommendations for HVAC, electrical, plumbing, and refrigeration "
    "field service operations.",
    instruction=INSTRUCTION,
    tools=[db_toolset],
    disallow_transfer_to_peers=True,
)
