# app/openai_utils.py

import os
from dotenv import load_dotenv
from litellm import completion
from app.prompts import SUMMARY_PROMPT

load_dotenv()

# ✅ Only use LiteLLM/Groq now
os.environ["LITELLM_API_KEY"] = os.getenv("LITELLM_API_KEY")

# Constants
TEMPERATURE = 0.1
MAX_TOKENS = 350
TOP_P = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0

SUPPORTED_MODELS = {
    "groq/llama3-8b-8192",
    "groq/llama-3.1-8b-instant",
    "groq/llama-3.1-70b-versatile"
}

def gpt_without_functions(model, stream=False, messages=[]):
    """Use Groq via LiteLLM to get completions."""
    if model not in SUPPORTED_MODELS:
        raise ValueError("Unsupported model.")
    response = completion(
        model=model,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
        stream=stream
    )
    return response

def summarise_conversation(history):
    """Summarise conversation history using Groq."""
    conversation = ""
    for item in history[-70:]:
        if 'user_input' in item:
            conversation += f"User: {item['user_input']}\n"
        if 'bot_response' in item:
            conversation += f"Bot: {item['bot_response']}\n"

    response = gpt_without_functions(
        model="groq/llama3-8b-8192",
        stream=False,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": conversation}
        ]
    )

    return response.choices[0].message.content.strip()
