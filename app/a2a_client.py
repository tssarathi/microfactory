import os
from uuid import uuid4

import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.types import (
    Artifact,
    DataPart,
    Message,
    Part,
    Role,
    TaskArtifactUpdateEvent,
    TextPart,
)
from dotenv import load_dotenv

load_dotenv()

COORDINATOR_URL = os.environ["COORDINATOR_URL"]


class CoordinatorClient:
    def __init__(self, url: str = COORDINATOR_URL):
        self._url = url
        self._httpx = httpx.AsyncClient(timeout=120.0)
        self._client = None

    async def _ensure_client(self):
        if self._client is None:
            config = ClientConfig(httpx_client=self._httpx)
            self._client = await ClientFactory.connect(self._url, client_config=config)
        return self._client

    async def complete(self, text: str, context_id: str) -> str:
        client = await self._ensure_client()
        message = Message(
            messageId=str(uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text=text))],
            contextId=context_id,
        )
        out: list[str] = []

        async for event in client.send_message(message):
            if isinstance(event, Message):
                for part in event.parts:
                    if isinstance(part.root, TextPart):
                        out.append(part.root.text)
            elif isinstance(event, tuple):
                task, update = event
                if isinstance(update, TaskArtifactUpdateEvent):
                    _append_response_text_from_artifact(update.artifact, out)
                elif update is None:
                    for artifact in task.artifacts or []:
                        _append_response_text_from_artifact(artifact, out)

        return "".join(out)

    async def close(self):
        if self._client:
            await self._client.close()
        await self._httpx.aclose()


def _append_response_text_from_artifact(artifact: Artifact, out: list[str]) -> None:
    for part in artifact.parts:
        root = part.root
        if isinstance(root, TextPart):
            if (root.metadata or {}).get("adk_thought", False):
                continue
            out.append(root.text)
        elif isinstance(root, DataPart):
            continue
