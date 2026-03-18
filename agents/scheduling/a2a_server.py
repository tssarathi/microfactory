import os

import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agents.scheduling.agent import root_agent

A2A_HOST = os.getenv("A2A_HOST", "localhost")

app = to_a2a(root_agent, host=A2A_HOST, port=8002, protocol="http")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
