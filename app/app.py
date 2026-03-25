import os
import uuid

import chainlit as cl
from a2a_client import CoordinatorClient
from dotenv import load_dotenv

load_dotenv()

TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+61 4XX XXX XXX")


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Open jobs",
            message="What open jobs do we have right now?",
        ),
        cl.Starter(
            label="Send a technician",
            message="I need someone for an emergency at Eagle Farm Cold Storage. Who's available?",
        ),
        cl.Starter(
            label="Safety procedure",
            message="What's the emergency procedure for a refrigerant leak on site?",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    cl.user_session.set("client", CoordinatorClient())


@cl.on_chat_end
async def on_chat_end():
    client = cl.user_session.get("client")
    if client:
        await client.close()


@cl.on_message
async def on_message(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    client = cl.user_session.get("client")

    async with cl.Step(name="Ana", type="run"):
        final_text = await client.complete(message.content, session_id)

    await cl.Message(content=final_text).send()
