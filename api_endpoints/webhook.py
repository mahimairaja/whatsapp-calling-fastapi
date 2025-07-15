from fastapi import APIRouter, Query, Response, status, Request
from datetime import datetime
import os
from dotenv import load_dotenv

from utils import message

load_dotenv()


VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


router = APIRouter(prefix="/webhook")

@router.get("/")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode",),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return Response(content=hub_challenge, status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.post("/")
async def receive_webhook(request: Request):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n\nWebhook received {timestamp}\n")
    body = await request.json()

    if_message_body = body.get("entry", [])

    try :
        received_message = if_message_body[0].get(
                                "changes", [])[0].get(
                                "value", {}).get(
                                "messages", [])[0].get(
                                "text", {}).get(
                                "body", "")
    except Exception as e:
        print(f"Error: {e}")
        received_message = None

    if received_message == "hi":
        values = if_message_body[0].get("changes", [])[0].get("value")
        recipient_id = values.get("contacts")[0].get("wa_id")
        phone_number_id = values.get("metadata").get("phone_number_id")

        response = message.send_message(
            recipient_id,
            phone_number_id,
            ACCESS_TOKEN,
            "Hello, how can I help you today?"
        )
        print(f"Response: {response!r}")

    print(body, end="\n\n")
    return Response(status_code=status.HTTP_200_OK)