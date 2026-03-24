import chainlit as cl
import uuid
import os
from a2a_client import send_message
from dotenv import load_dotenv

load_dotenv()

TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+61 4XX XXX XXX")


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="WO-1 parts and procedure",
            message="WO-1 AC not cooling at Brisbane City Tower. What parts do I need and what's the troubleshooting procedure?",
        ),
        cl.Starter(
            label="Dispatch for Eagle Farm",
            message="Who's qualified for Eagle Farm Cold Storage and what's the site safety protocol?",
        ),
        cl.Starter(
            label="WO-3 full dispatch",
            message="WO-3 freezer compressor alarm. What's the issue, who can I send, and what safety applies?",
        ),
        cl.Starter(
            label="Refrigerant leak response",
            message="What's the emergency procedure for a refrigerant leak on site?",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("session_id", str(uuid.uuid4()))


@cl.on_message
async def on_message(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    async with cl.Step(name="Coordinator") as step:
        step.input = message.content
        response = await send_message(message.content, session_id)
        step.output = response
    await cl.Message(content=response).send()
