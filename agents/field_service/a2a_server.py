import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agents.field_service.agent import root_agent

app = to_a2a(root_agent, host="0.0.0.0", port=8001, protocol="http")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
