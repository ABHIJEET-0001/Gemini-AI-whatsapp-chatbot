import os
import json
from datetime import datetime
from dotenv import load_dotenv

from fastapi import Form, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from twilio.rest import Client

from app.cookies_utils import set_cookies, get_cookies, clear_cookies
from app.prompts import SYSTEM_PROMPT
from app.openai_utils import gpt_without_functions, summarise_conversation
from app.redis_utils import redis_conn
from app.logger_utils import logger

# ✅ Load env variables
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

app = FastAPI(
    title="Twilio-Groq-WhatsApp-Bot",
    description="Twilio WhatsApp Bot using Groq + LiteLLM",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "you@example.com",
    }
)

# ✅ Allow all CORS
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

def respond(to_number, message) -> None:
    """Send a WhatsApp message using Twilio."""
    from_whatsapp_number = "whatsapp:" + TWILIO_WHATSAPP_NUMBER
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_number
    )

@app.post('/whatsapp-endpoint')
async def whatsapp_endpoint(request: Request, From: str = Form(...), Body: str = Form(...)):
    logger.info("📲 WhatsApp endpoint triggered")
    logger.info(f"Request: {request}")
    logger.info(f"Body: {Body}")
    logger.info(f"From: {From}")

    query = Body
    phone_no = From.replace('whatsapp:+', '')
    chat_session_id = phone_no

    # ✅ Load history from Redis
    history = get_cookies(redis_conn, f'whatsapp_twilio_demo_{chat_session_id}_history') or []
    if history:
        history = json.loads(history)

    history.append({"role": 'user', "user_input": query})

    # ✅ Summarize conversation
    history_summary = summarise_conversation(history)

    system_prompt = SYSTEM_PROMPT.format(
        history_summary=history_summary,
        today=datetime.now().date()
    )

    # ✅ Get response from Groq (via LiteLLM)
    response = gpt_without_functions(
        model="groq/llama3-8b-8192",
        stream=False,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'assistant', 'content': "Hi there, how can I help you?"}
        ] + history
    )

    chatbot_response = response.choices[0].message.content.strip()

    history.append({'role': 'assistant', 'bot_response': chatbot_response})

    # ✅ Save updated history
    set_cookies(redis_conn, name=f'whatsapp_twilio_demo_{chat_session_id}_history', value=json.dumps(history))

    # ✅ Respond via WhatsApp
    respond(From, chatbot_response)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3002, reload=True)
