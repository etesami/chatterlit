# utils.py
import base64
import tiktoken
import os
from models import MODEL_OPTIONS
from openai import OpenAI

# Tokenizer: always use the current selected_model
def count_tokens(message, model):
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")

    if isinstance(message["content"], str):
        # Standard text-only messages
        return len(enc.encode(message["content"]))

    elif isinstance(message["content"], list):
        # Multimodal: count only the text parts
        token_count = 0
        for part in message["content"]:
            if part["type"] == "text":
                token_count += len(enc.encode(part["text"]))
        return token_count

    return 0 


def get_content(message):
    if isinstance(message["content"], list):
        for part in message["content"]:
            if part["type"] == "text":
                return part["text"]
    elif isinstance(message["content"], str):
        return message["content"]
    else:
        return "Error: user message not detected."

def truncate_message(text, max_length=200):
    return text if len(text) <= max_length else text[:max_length] + "..."

def encode_images(files):
    for f in files:
        yield {
            "type": "image_url",
            "image_url": {
                "url": f"data:{f.type};base64,{base64.b64encode(f.read()).decode()}"
            },
        }

def init_client(model):
    keys = {
        "grok": ("GROK_API_KEY", "https://api.x.ai/v1"),
        "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    }
    for prefix, (env, url) in keys.items():
        if model.startswith(prefix):
            if not (key := os.getenv(env)):
                st.error(f"{env} not set."); st.stop()
            return OpenAI(api_key=key, base_url=url)
    if not (key := os.getenv("OPENAI_API_KEY")):
        st.error("OPENAI_API_KEY not set."); st.stop()
    return OpenAI(api_key=key)

