import json
from fastapi import FastAPI, Request
from .ring_test import set_dnd

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):

    print("=" * 50)

    body = await request.body()

    body_str = body.decode("utf-8")

    # Remove RingCentral's non-breaking spaces
    body_str = body_str.replace("\u00A0", " ")

    print(body_str)

    data = json.loads(body_str)

    command = data["command"].strip().upper()
    extension_id = data["extensionId"].strip()

    print(f"Command: {command}")
    print(f"Extension ID: {extension_id}")

    if command == "DAYOFF":
        set_dnd(extension_id, True)

        return {
            "status": "success",
            "action": "dnd_enabled"
        }

    elif command == "BACK":
        set_dnd(extension_id, False)

        return {
            "status": "success",
            "action": "dnd_disabled"
        }

    return {
        "status": "ignored",
        "command": command
    }