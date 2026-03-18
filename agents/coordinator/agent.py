from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from field_service.agent import root_agent as field_service_agent
from scheduling.agent import root_agent as scheduling_agent
from knowledge.agent import root_agent as knowledge_agent

from .instruction import INSTRUCTION

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3.5:9b"),
    name="coordinator_agent",
    description="Operations coordinator for The Good Trades Co. field service. Routes queries "
    "to specialist agents — Field Service for work orders, equipment, parts, and "
    "customers; Scheduling for technician availability, dispatch, and certifications; "
    "Knowledge for procedures, safety protocols, and technical documentation. "
    "Synthesises multi-agent responses into unified answers.",
    instruction=INSTRUCTION,
    sub_agents=[field_service_agent, scheduling_agent, knowledge_agent],
)
