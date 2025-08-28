from fastapi import FastAPI, Request
import requests

app = FastAPI()

# 🔑 Replace with your actual Bot User OAuth Token (from Slack app settings)
SLACK_BOT_TOKEN = "xoxb-abcd"

@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    print("Slack event:", data)  # Debug logs

    # 1️⃣ Slack URL verification (first time setup)
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    # 2️⃣ Handle Slack events
    if "event" in data:
        event = data["event"]

        if "bot_id" in event:
        # Ignore messages from any bot
            return

        # Only reply to user messages (ignore bot/system messages)
        if event.get("type") == "message" and "subtype" not in event:
            user_text = event.get("text")
            channel_id = event.get("channel")
            user_id = event.get("user")

            reply_text = f"👋 Hey <@{user_id}>, you said: {user_text}"

            # Call Slack API to reply
            response = requests.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
                json={"channel": channel_id, "text": reply_text}
            )
            print("Slack API response:", response.json())

    return {"ok": True}
