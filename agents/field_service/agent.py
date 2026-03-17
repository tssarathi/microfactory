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
        "search_work_orders",
        "get_work_order_details",
        "get_available_technicians",
        "search_parts",
        "get_customer_details",
        "get_customer_equipment",
        "get_equipment_details",
    ],
)

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3:8b"),
    name="field_service_agent",
    description="Manages work orders, equipment, parts inventory, and technical context for field service operations.",
    instruction=INSTRUCTION,
    tools=[db_toolset],
)
