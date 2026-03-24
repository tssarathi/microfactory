from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

import os
from .instruction import INSTRUCTION

FIELD_SERVICE_HOST = os.getenv("FIELD_SERVICE_HOST", "localhost")
SCHEDULING_HOST = os.getenv("SCHEDULING_HOST", "localhost")
KNOWLEDGE_HOST = os.getenv("KNOWLEDGE_HOST", "localhost")

field_service_agent = RemoteA2aAgent(
    name="field_service_agent",
    description=(
        "Field service operations specialist. Manages work orders, equipment "
        "records, parts inventory, and customer context for HVAC, electrical, "
        "plumbing, and refrigeration service jobs. Use this agent for work order "
        "lookups, equipment warranty and service history, parts stock checks, "
        "customer details, and cross-referencing parts usage across jobs."
    ),
    agent_card=f"http://{FIELD_SERVICE_HOST}:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

scheduling_agent = RemoteA2aAgent(
    name="scheduling_agent",
    description=(
        "Scheduling and dispatch advisory. Manages technician availability, "
        "schedule lookups, certification compliance checks, and dispatch "
        "recommendations for HVAC, electrical, plumbing, and refrigeration "
        "field service operations. Use this agent for technician availability "
        "checks, who to send on a job, scheduling slots, dispatch decisions, "
        "and certification compliance verification."
    ),
    agent_card=f"http://{SCHEDULING_HOST}:8002{AGENT_CARD_WELL_KNOWN_PATH}",
)

knowledge_agent = RemoteA2aAgent(
    name="knowledge_agent",
    description=(
        "Technical knowledge specialist. Handles troubleshooting procedures, "
        "safety protocols, preventive maintenance schedules, Australian Standards "
        "references, and company SOPs for HVAC, electrical, plumbing, and "
        "refrigeration. Use this agent for HOW-TO questions, safety procedures, "
        "troubleshooting steps, and technical documentation lookups."
    ),
    agent_card=f"http://{KNOWLEDGE_HOST}:8003{AGENT_CARD_WELL_KNOWN_PATH}",
)

root_agent = Agent(
    model=LiteLlm(model="openai/qwen3.5:35b"),
    name="coordinator_agent",
    description="Operations coordinator for The Good Trades Co. field service. Routes queries "
    "to specialist agents — Field Service for work orders, equipment, parts, and "
    "customers; Scheduling for technician availability, dispatch, and certifications; "
    "Knowledge for procedures, safety protocols, and technical documentation. "
    "Synthesises multi-agent responses into unified answers.",
    instruction=INSTRUCTION,
    sub_agents=[field_service_agent, scheduling_agent, knowledge_agent],
)
