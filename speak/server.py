from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import PlainTextResponse
import uvicorn
import json

app = FastAPI()


@app.post("/twiml")
async def twiml(request: Request):
    host = request.headers.get("host")
    ws_url = f"wss://{host}/audio-stream"

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Hi there! Connecting you to Ana now. Please hold on.</Say>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>"""

    return PlainTextResponse(content=twiml_response, media_type="application/xml")


@app.websocket("/audio-stream")
async def media_stream(ws: WebSocket):
    await ws.accept()
    print("[Twilio] WebSocket connected")
    stream_sid = None

    try:
        async for message in ws.iter_text():
            data = json.loads(message)
            event = data["event"]

            if event == "connected":
                print("[Twilio] Stream connected")

            elif event == "start":
                stream_sid = data["start"]["streamSid"]
                print(f"[Twilio] Stream started with SID: {stream_sid}")

            elif event == "media":
                payload = data["media"]["payload"]
                print(f"[Twilio] Audio chunk: {len(payload)} base64 chars", end="\r")

            elif event == "stop":
                print("\n[Twilio] Stream stopped")
                break

    except Exception as e:
        print(f"[Twilio] Error: {e}")
    finally:
        print("[Twilio] WebSocket closed")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
