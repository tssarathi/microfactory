import os
import httpx
from a2a.client import ClientFactory, ClientConfig, create_text_message_object
from a2a.types import Message, TextPart
from dotenv import load_dotenv

load_dotenv()

COORDINATOR_URL = os.environ["COORDINATOR_URL"]


async def send_message(text: str, session_id: str) -> str:
    config = ClientConfig(httpx_client=httpx.AsyncClient(timeout=120.0))
    client = await ClientFactory.connect(COORDINATOR_URL, client_config=config)
    message = create_text_message_object(content=text)
    result_parts = []
    async for event in client.send_message(message):
        if isinstance(event, Message):
            for part in event.parts:
                if isinstance(part.root, TextPart):
                    result_parts.append(part.root.text)
        elif isinstance(event, tuple):
            task, _ = event
            for artifact in (task.artifacts or []):
                for part in artifact.parts:
                    if isinstance(part.root, TextPart) and not (part.root.metadata or {}).get("adk_thought"):
                        result_parts.append(part.root.text)
    await client.close()
    return "".join(result_parts)
