from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from pathlib import Path


from .instruction import INSTRUCTION

TOOLS_DIR = Path(__file__).resolve().parents[2] / "tools"

kb_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "python", str(TOOLS_DIR / "knowledge_base/server.py")],
        ),
    ),
    tool_filter=[
        "search_knowledge",
    ],
)

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3:8b"),
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
